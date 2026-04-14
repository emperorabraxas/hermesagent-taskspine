"""Redis service — full integration for spider.Web.

Features:
  - Pub/Sub: real-time spider notifications (replaces polling)
  - Streams: event sourcing for all agent actions (audit trail)
  - Hashes: live spider state (sub-ms reads)
  - Sorted Sets: XP leaderboard, model usage ranking, P&L ranking
  - Rate Limiting: API cost control per spider, per provider
  - Caching: semantic cache (already exists), session cache, config cache
  - Pipelining: batch operations for performance

Architecture:
  - All spiders publish events to Redis
  - Dashboard subscribes via Pub/Sub for instant updates
  - Streams provide persistent, replayable event log
  - Hashes are the source of truth for current spider state
"""
from __future__ import annotations

import json
import logging
import time
from typing import Any, AsyncIterator

import redis.asyncio as aioredis

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)


class RedisService:
    """Full Redis integration for spider.Web."""

    def __init__(self):
        self._redis: aioredis.Redis | None = None
        self._pubsub: aioredis.client.PubSub | None = None

    async def connect(self, url: str | None = None) -> bool:
        """Connect to Redis."""
        try:
            url = url or get_settings().redis_url
            if not url:
                logger.warning("No REDIS_URL configured — Redis features disabled")
                return False
            self._redis = aioredis.from_url(url, decode_responses=True)
            await self._redis.ping()
            logger.info("Redis service connected")
            return True
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self._redis = None
            return False

    @property
    def connected(self) -> bool:
        return self._redis is not None

    # ══════════════════════════════════════════════════════════════
    # PUB/SUB — Real-time spider notifications
    # ══════════════════════════════════════════════════════════════

    async def publish(self, channel: str, data: dict) -> int:
        """Publish an event to a channel.

        Channels:
          spider:status — spider state changes (active/idle)
          spider:message — agent chat messages
          spider:action — tool calls, trades, file ops
          spider:alert — HITL approvals, errors, warnings
          dashboard:update — stats refresh triggers
        """
        if not self._redis:
            return 0
        payload = json.dumps(data, default=str)
        return await self._redis.publish(channel, payload)

    async def subscribe(self, *channels: str) -> aioredis.client.PubSub:
        """Subscribe to one or more channels. Returns PubSub object for iteration."""
        if not self._redis:
            raise ConnectionError("Redis not connected")
        pubsub = self._redis.pubsub()
        await pubsub.subscribe(*channels)
        return pubsub

    async def listen(self, pubsub: aioredis.client.PubSub) -> AsyncIterator[dict]:
        """Async iterator over pubsub messages."""
        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    yield json.loads(message["data"])
                except (json.JSONDecodeError, TypeError):
                    yield {"raw": message["data"]}

    # ── Convenience publishers ────────────────────────────────────

    async def publish_spider_status(self, spider: str, status: str, text: str = "") -> int:
        """Publish a spider status change. Dashboard picks this up instantly."""
        return await self.publish("spider:status", {
            "spider": spider, "status": status, "text": text,
            "ts": time.time(),
        })

    async def publish_spider_message(self, spider: str, text: str, role: str = "assistant") -> int:
        """Publish a spider chat message for WEB COMMS."""
        return await self.publish("spider:message", {
            "spider": spider, "text": text, "role": role,
            "ts": time.time(),
        })

    async def publish_spider_action(self, spider: str, action: str, detail: str = "") -> int:
        """Publish a spider action (tool call, trade, etc.)."""
        return await self.publish("spider:action", {
            "spider": spider, "action": action, "detail": detail,
            "ts": time.time(),
        })

    async def publish_alert(self, spider: str, level: str, message: str) -> int:
        """Publish an alert (HITL approval, error, warning)."""
        return await self.publish("spider:alert", {
            "spider": spider, "level": level, "message": message,
            "ts": time.time(),
        })

    # ══════════════════════════════════════════════════════════════
    # STREAMS — Event sourcing / audit trail
    # ══════════════════════════════════════════════════════════════

    async def log_event(self, stream: str, data: dict, maxlen: int = 10000) -> str:
        """Append an event to a Redis stream.

        Streams:
          events:spider — all spider activity
          events:trade — trading actions
          events:chat — chat messages
          events:system — system events (startup, config changes)

        Returns the stream entry ID.
        """
        if not self._redis:
            return ""
        # Flatten nested dicts to strings for Redis stream compatibility
        flat = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in data.items()}
        flat["ts"] = str(time.time())
        return await self._redis.xadd(stream, flat, maxlen=maxlen)

    async def read_events(
        self, stream: str, count: int = 50, start: str = "-", end: str = "+",
    ) -> list[dict]:
        """Read events from a stream (most recent)."""
        if not self._redis:
            return []
        entries = await self._redis.xrevrange(stream, max=end, min=start, count=count)
        return [
            {"id": entry_id, **{k: v for k, v in fields.items()}}
            for entry_id, fields in entries
        ]

    async def stream_length(self, stream: str) -> int:
        """Get the number of entries in a stream."""
        if not self._redis:
            return 0
        return await self._redis.xlen(stream)

    async def create_consumer_group(
        self, stream: str, group: str, start_id: str = "0",
    ) -> bool:
        """Create a consumer group for a stream."""
        if not self._redis:
            return False
        try:
            await self._redis.xgroup_create(stream, group, id=start_id, mkstream=True)
            return True
        except aioredis.ResponseError as e:
            if "BUSYGROUP" in str(e):
                return True  # Already exists
            raise

    async def read_group(
        self, stream: str, group: str, consumer: str, count: int = 10,
    ) -> list[dict]:
        """Read new events as a consumer in a group."""
        if not self._redis:
            return []
        result = await self._redis.xreadgroup(group, consumer, {stream: ">"}, count=count)
        events = []
        for _, entries in result:
            for entry_id, fields in entries:
                events.append({"id": entry_id, **fields})
        return events

    async def ack_event(self, stream: str, group: str, *ids: str) -> int:
        """Acknowledge processed events in a consumer group."""
        if not self._redis:
            return 0
        return await self._redis.xack(stream, group, *ids)

    # ══════════════════════════════════════════════════════════════
    # HASHES — Live spider state (sub-millisecond reads)
    # ══════════════════════════════════════════════════════════════

    async def set_spider_state(self, spider: str, state: dict) -> None:
        """Set the full state for a spider. Overwrites all fields."""
        if not self._redis:
            return
        key = f"spider:{spider}"
        flat = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in state.items()}
        await self._redis.hset(key, mapping=flat)

    async def update_spider_field(self, spider: str, field: str, value: Any) -> None:
        """Update a single field in a spider's state."""
        if not self._redis:
            return
        key = f"spider:{spider}"
        val = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        await self._redis.hset(key, field, val)

    async def get_spider_state(self, spider: str) -> dict:
        """Get the full state for a spider."""
        if not self._redis:
            return {}
        key = f"spider:{spider}"
        return await self._redis.hgetall(key) or {}

    async def get_all_spider_states(self) -> dict[str, dict]:
        """Get state for all spiders."""
        if not self._redis:
            return {}
        spiders = ["cockpit", "scholar", "oracle", "code_team", "ops",
                    "automator", "warroom", "money_maker", "lab"]
        result = {}
        pipe = self._redis.pipeline()
        for s in spiders:
            pipe.hgetall(f"spider:{s}")
        states = await pipe.execute()
        for s, state in zip(spiders, states):
            if state:
                result[s] = state
        return result

    # ══════════════════════════════════════════════════════════════
    # SORTED SETS — Leaderboards & Rankings
    # ══════════════════════════════════════════════════════════════

    async def update_leaderboard(self, board: str, member: str, score: float) -> None:
        """Add/update a member's score on a leaderboard.

        Boards:
          leaderboard:xp — spider XP rankings
          leaderboard:tasks — task completion count
          leaderboard:trades — trading P&L
          leaderboard:usage — model usage (token count)
        """
        if not self._redis:
            return
        await self._redis.zadd(board, {member: score})

    async def increment_score(self, board: str, member: str, amount: float) -> float:
        """Increment a member's score. Returns new score."""
        if not self._redis:
            return 0
        return await self._redis.zincrby(board, amount, member)

    async def get_leaderboard(self, board: str, top_n: int = 10, desc: bool = True) -> list[dict]:
        """Get top N entries from a leaderboard."""
        if not self._redis:
            return []
        if desc:
            entries = await self._redis.zrevrange(board, 0, top_n - 1, withscores=True)
        else:
            entries = await self._redis.zrange(board, 0, top_n - 1, withscores=True)
        return [{"member": member, "score": score} for member, score in entries]

    async def get_rank(self, board: str, member: str, desc: bool = True) -> int | None:
        """Get a member's rank (0-indexed). Returns None if not on board."""
        if not self._redis:
            return None
        if desc:
            return await self._redis.zrevrank(board, member)
        return await self._redis.zrank(board, member)

    # ══════════════════════════════════════════════════════════════
    # RATE LIMITING — API cost control
    # ══════════════════════════════════════════════════════════════

    async def check_rate_limit(
        self, key: str, max_requests: int = 60, window_seconds: int = 60,
    ) -> tuple[bool, int]:
        """Sliding window rate limiter.

        Keys:
          ratelimit:openai — global OpenAI rate limit
          ratelimit:openai:scholar — per-spider OpenAI limit
          ratelimit:api:user123 — per-user API limit

        Returns: (allowed: bool, current_count: int)
        """
        if not self._redis:
            return True, 0
        now = time.time()
        pipe = self._redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - window_seconds)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window_seconds)
        results = await pipe.execute()
        count = results[2]
        return count <= max_requests, count

    async def get_rate_limit_remaining(
        self, key: str, max_requests: int = 60, window_seconds: int = 60,
    ) -> int:
        """How many requests remain in the current window."""
        if not self._redis:
            return max_requests
        now = time.time()
        await self._redis.zremrangebyscore(key, 0, now - window_seconds)
        count = await self._redis.zcard(key)
        return max(0, max_requests - count)

    # ══════════════════════════════════════════════════════════════
    # CACHING — General purpose
    # ══════════════════════════════════════════════════════════════

    async def cache_set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set a cached value with TTL."""
        if not self._redis:
            return
        data = json.dumps(value, default=str) if not isinstance(value, str) else value
        await self._redis.setex(key, ttl, data)

    async def cache_get(self, key: str) -> Any | None:
        """Get a cached value. Returns None if not found/expired."""
        if not self._redis:
            return None
        raw = await self._redis.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return raw

    async def cache_delete(self, key: str) -> bool:
        """Delete a cached value."""
        if not self._redis:
            return False
        return bool(await self._redis.delete(key))

    # ══════════════════════════════════════════════════════════════
    # PIPELINING — Batch operations
    # ══════════════════════════════════════════════════════════════

    def pipeline(self):
        """Get a Redis pipeline for batching commands."""
        if not self._redis:
            return None
        return self._redis.pipeline()

    # ══════════════════════════════════════════════════════════════
    # INFO / HEALTH
    # ══════════════════════════════════════════════════════════════

    async def info(self) -> dict:
        """Get Redis server info (memory, clients, etc.)."""
        if not self._redis:
            return {}
        raw = await self._redis.info()
        return {
            "used_memory_human": raw.get("used_memory_human", ""),
            "connected_clients": raw.get("connected_clients", 0),
            "total_commands_processed": raw.get("total_commands_processed", 0),
            "keyspace_hits": raw.get("keyspace_hits", 0),
            "keyspace_misses": raw.get("keyspace_misses", 0),
            "uptime_seconds": raw.get("uptime_in_seconds", 0),
        }

    async def key_count(self) -> int:
        """Total number of keys."""
        if not self._redis:
            return 0
        return await self._redis.dbsize()


# Singleton
_service: RedisService | None = None


async def get_redis_service() -> RedisService:
    global _service
    if _service is None:
        _service = RedisService()
        await _service.connect()
    return _service
