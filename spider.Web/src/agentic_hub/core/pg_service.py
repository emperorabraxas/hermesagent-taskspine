"""PostgreSQL advanced features service for spider.Web.

Features:
  - Full-text search across conversations and entities
  - LISTEN/NOTIFY for real-time dashboard updates
  - Materialized views for pre-computed stats
  - Window functions for time-series analytics
  - JSONB indexing for fast JSON queries
  - pg_trgm fuzzy matching for entity lookup
  - Partitioning support for time-series tables

All queries use asyncpg for direct SQL execution (bypassing SQLAlchemy
for performance-critical paths).
"""
from __future__ import annotations

import logging
from typing import Any

import asyncpg

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)


class PostgresService:
    """Advanced PostgreSQL features for spider.Web."""

    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self, dsn: str | None = None) -> bool:
        """Create a connection pool."""
        try:
            dsn = dsn or get_settings().database_url
            if not dsn:
                logger.warning("No DATABASE_URL configured — Postgres features disabled")
                return False
            # Convert SQLAlchemy URL format to asyncpg format
            dsn = dsn.replace("postgresql+asyncpg://", "postgresql://")
            dsn = dsn.replace("postgresql+psycopg2://", "postgresql://")
            self._pool = await asyncpg.create_pool(dsn, min_size=2, max_size=10)
            logger.info("Postgres service connected (pool: 2-10)")
            return True
        except Exception as e:
            logger.warning(f"Postgres connection failed: {e}")
            self._pool = None
            return False

    @property
    def connected(self) -> bool:
        return self._pool is not None

    # ══════════════════════════════════════════════════════════════
    # SETUP — Extensions & Indexes (run once)
    # ══════════════════════════════════════════════════════════════

    async def setup_extensions(self) -> None:
        """Enable required PostgreSQL extensions. Safe to call multiple times."""
        if not self._pool:
            return
        async with self._pool.acquire() as conn:
            # Full-text search (built-in, just needs index)
            # pg_trgm for fuzzy matching
            await conn.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
            logger.info("pg_trgm extension enabled")

    async def setup_indexes(self) -> None:
        """Create advanced indexes for performance. Safe to call multiple times."""
        if not self._pool:
            return
        async with self._pool.acquire() as conn:
            # Full-text search index on messages
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_fts
                ON messages USING GIN (to_tsvector('english', content))
            """)
            # Full-text search index on entities
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_entities_fts
                ON entities USING GIN (to_tsvector('english', name || ' ' || COALESCE(description, '')))
            """)
            # Trigram index on entity names for fuzzy matching
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_entities_trgm
                ON entities USING GIN (name gin_trgm_ops)
            """)
            # JSONB GIN index on roles.permissions
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_roles_permissions
                ON roles USING GIN (permissions)
            """)
            # Timestamp indexes for time-series queries
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_created
                ON messages (created_at DESC)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_xp_events_created
                ON xp_events (created_at DESC)
            """)
            logger.info("Advanced indexes created")

    # ══════════════════════════════════════════════════════════════
    # FULL-TEXT SEARCH
    # ══════════════════════════════════════════════════════════════

    async def search_messages(
        self, query: str, limit: int = 20, conversation_id: int | None = None,
    ) -> list[dict]:
        """Full-text search across chat messages.

        Uses PostgreSQL's tsvector/tsquery for ranked results.
        """
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            sql = """
                SELECT m.id, m.role, m.content, m.agent, m.created_at,
                       ts_rank(to_tsvector('english', m.content), plainto_tsquery('english', $1)) AS rank
                FROM messages m
                WHERE to_tsvector('english', m.content) @@ plainto_tsquery('english', $1)
            """
            params: list[Any] = [query]
            if conversation_id:
                sql += " AND m.conversation_id = $2"
                params.append(conversation_id)
            sql += " ORDER BY rank DESC LIMIT $" + str(len(params) + 1)
            params.append(limit)
            rows = await conn.fetch(sql, *params)
            return [dict(r) for r in rows]

    async def search_entities(
        self, query: str, entity_type: str | None = None, limit: int = 20,
    ) -> list[dict]:
        """Full-text search across entities (knowledge graph)."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            sql = """
                SELECT id, name, entity_type, description, mention_count,
                       ts_rank(to_tsvector('english', name || ' ' || COALESCE(description, '')),
                               plainto_tsquery('english', $1)) AS rank
                FROM entities
                WHERE to_tsvector('english', name || ' ' || COALESCE(description, ''))
                      @@ plainto_tsquery('english', $1)
            """
            params: list[Any] = [query]
            if entity_type:
                sql += " AND entity_type = $2"
                params.append(entity_type)
            sql += " ORDER BY rank DESC LIMIT $" + str(len(params) + 1)
            params.append(limit)
            rows = await conn.fetch(sql, *params)
            return [dict(r) for r in rows]

    async def fuzzy_match_entity(self, name: str, limit: int = 5) -> list[dict]:
        """Fuzzy match entity names using pg_trgm (e.g., "AAPL" ≈ "Apple")."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, name, entity_type, description,
                       similarity(name, $1) AS sim
                FROM entities
                WHERE similarity(name, $1) > 0.2
                ORDER BY sim DESC
                LIMIT $2
            """, name, limit)
            return [dict(r) for r in rows]

    # ══════════════════════════════════════════════════════════════
    # LISTEN/NOTIFY — Real-time triggers
    # ══════════════════════════════════════════════════════════════

    async def setup_notify_triggers(self) -> None:
        """Create triggers that fire NOTIFY on key table changes."""
        if not self._pool:
            return
        async with self._pool.acquire() as conn:
            # Trigger function for new messages
            await conn.execute("""
                CREATE OR REPLACE FUNCTION notify_new_message()
                RETURNS TRIGGER AS $$
                BEGIN
                    PERFORM pg_notify('new_message', json_build_object(
                        'id', NEW.id,
                        'role', NEW.role,
                        'agent', NEW.agent,
                        'conversation_id', NEW.conversation_id
                    )::text);
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """)
            await conn.execute("""
                DROP TRIGGER IF EXISTS trg_new_message ON messages;
                CREATE TRIGGER trg_new_message
                AFTER INSERT ON messages
                FOR EACH ROW EXECUTE FUNCTION notify_new_message();
            """)
            # Trigger for XP events
            await conn.execute("""
                CREATE OR REPLACE FUNCTION notify_xp_event()
                RETURNS TRIGGER AS $$
                BEGIN
                    PERFORM pg_notify('xp_event', json_build_object(
                        'agent', NEW.agent,
                        'xp_amount', NEW.xp_amount,
                        'reason', NEW.reason
                    )::text);
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """)
            await conn.execute("""
                DROP TRIGGER IF EXISTS trg_xp_event ON xp_events;
                CREATE TRIGGER trg_xp_event
                AFTER INSERT ON xp_events
                FOR EACH ROW EXECUTE FUNCTION notify_xp_event();
            """)
            # Trigger for new achievements
            await conn.execute("""
                CREATE OR REPLACE FUNCTION notify_achievement()
                RETURNS TRIGGER AS $$
                BEGIN
                    PERFORM pg_notify('achievement', json_build_object(
                        'user_id', NEW.user_id,
                        'achievement_key', NEW.achievement_key
                    )::text);
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """)
            await conn.execute("""
                DROP TRIGGER IF EXISTS trg_achievement ON achievements;
                CREATE TRIGGER trg_achievement
                AFTER INSERT ON achievements
                FOR EACH ROW EXECUTE FUNCTION notify_achievement();
            """)
            logger.info("LISTEN/NOTIFY triggers created")

    async def listen(self, *channels: str):
        """Listen to PostgreSQL NOTIFY channels. Returns connection for async iteration.

        Usage:
            conn = await pg.listen('new_message', 'xp_event')
            async for notify in conn:
                print(notify.channel, notify.payload)
        """
        if not self._pool:
            return None
        conn = await self._pool.acquire()
        for ch in channels:
            await conn.add_listener(ch, lambda conn, pid, channel, payload: None)
        return conn

    # ══════════════════════════════════════════════════════════════
    # MATERIALIZED VIEWS — Pre-computed stats
    # ══════════════════════════════════════════════════════════════

    async def setup_materialized_views(self) -> None:
        """Create materialized views for dashboard stats."""
        if not self._pool:
            return
        async with self._pool.acquire() as conn:
            # Spider activity summary
            await conn.execute("""
                CREATE MATERIALIZED VIEW IF NOT EXISTS mv_spider_stats AS
                SELECT
                    agent,
                    COUNT(*) as total_messages,
                    SUM(tokens_in) as total_tokens_in,
                    SUM(tokens_out) as total_tokens_out,
                    AVG(latency_ms) as avg_latency_ms,
                    MAX(created_at) as last_active
                FROM messages
                WHERE role = 'assistant'
                GROUP BY agent
            """)
            # Daily XP summary
            await conn.execute("""
                CREATE MATERIALIZED VIEW IF NOT EXISTS mv_daily_xp AS
                SELECT
                    DATE(created_at) as day,
                    agent,
                    SUM(xp_amount) as xp_earned,
                    COUNT(*) as actions
                FROM xp_events
                GROUP BY DATE(created_at), agent
                ORDER BY day DESC
            """)
            # Entity popularity
            await conn.execute("""
                CREATE MATERIALIZED VIEW IF NOT EXISTS mv_entity_popular AS
                SELECT
                    e.id, e.name, e.entity_type, e.mention_count,
                    COUNT(em.id) as recent_mentions
                FROM entities e
                LEFT JOIN entity_mentions em ON em.entity_id = e.id
                    AND em.created_at > NOW() - INTERVAL '7 days'
                GROUP BY e.id, e.name, e.entity_type, e.mention_count
                ORDER BY recent_mentions DESC
            """)
            logger.info("Materialized views created")

    async def refresh_materialized_views(self) -> None:
        """Refresh all materialized views (call periodically)."""
        if not self._pool:
            return
        async with self._pool.acquire() as conn:
            await conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_spider_stats")
            await conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_xp")
            await conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_entity_popular")

    async def get_spider_stats(self) -> list[dict]:
        """Get pre-computed spider activity stats."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM mv_spider_stats ORDER BY total_messages DESC")
            return [dict(r) for r in rows]

    async def get_daily_xp(self, days: int = 30) -> list[dict]:
        """Get daily XP summary."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM mv_daily_xp WHERE day > NOW() - $1::interval
            """, f"{days} days")
            return [dict(r) for r in rows]

    async def get_popular_entities(self, limit: int = 20) -> list[dict]:
        """Get most referenced entities in the last 7 days."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM mv_entity_popular LIMIT $1", limit)
            return [dict(r) for r in rows]

    # ══════════════════════════════════════════════════════════════
    # ANALYTICS — Window functions
    # ══════════════════════════════════════════════════════════════

    async def get_xp_trend(self, agent: str | None = None, days: int = 30) -> list[dict]:
        """Get XP trend with running total (window function)."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            sql = """
                SELECT
                    DATE(created_at) as day,
                    SUM(xp_amount) as daily_xp,
                    SUM(SUM(xp_amount)) OVER (ORDER BY DATE(created_at)) as cumulative_xp,
                    LAG(SUM(xp_amount)) OVER (ORDER BY DATE(created_at)) as prev_day_xp
                FROM xp_events
                WHERE created_at > NOW() - $1::interval
            """
            params: list[Any] = [f"{days} days"]
            if agent:
                sql += " AND agent = $2"
                params.append(agent)
            sql += " GROUP BY DATE(created_at) ORDER BY day"
            rows = await conn.fetch(sql, *params)
            return [dict(r) for r in rows]

    async def get_spider_response_times(self, limit: int = 100) -> list[dict]:
        """Get response time percentiles per spider (analytics)."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT
                    agent,
                    COUNT(*) as count,
                    AVG(latency_ms) as avg_ms,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms) as p50_ms,
                    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) as p95_ms,
                    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) as p99_ms,
                    MIN(latency_ms) as min_ms,
                    MAX(latency_ms) as max_ms
                FROM messages
                WHERE role = 'assistant' AND latency_ms > 0
                GROUP BY agent
                ORDER BY avg_ms
            """)
            return [dict(r) for r in rows]

    async def get_conversation_activity(self, days: int = 7) -> list[dict]:
        """Conversations per day with message counts (time-series)."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT
                    DATE(c.created_at) as day,
                    COUNT(DISTINCT c.id) as conversations,
                    COUNT(m.id) as messages,
                    SUM(m.tokens_in + m.tokens_out) as total_tokens
                FROM conversations c
                LEFT JOIN messages m ON m.conversation_id = c.id
                WHERE c.created_at > NOW() - $1::interval
                GROUP BY DATE(c.created_at)
                ORDER BY day DESC
            """, f"{days} days")
            return [dict(r) for r in rows]

    # ══════════════════════════════════════════════════════════════
    # RAW QUERY — For custom analytics
    # ══════════════════════════════════════════════════════════════

    async def query(self, sql: str, *args) -> list[dict]:
        """Execute a raw SQL query. Use for custom analytics."""
        if not self._pool:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(sql, *args)
            return [dict(r) for r in rows]

    async def execute(self, sql: str, *args) -> str:
        """Execute a raw SQL command (INSERT, UPDATE, DDL). Returns status."""
        if not self._pool:
            return "not connected"
        async with self._pool.acquire() as conn:
            return await conn.execute(sql, *args)


# Singleton
_service: PostgresService | None = None


async def get_pg_service() -> PostgresService:
    global _service
    if _service is None:
        _service = PostgresService()
        await _service.connect()
    return _service
