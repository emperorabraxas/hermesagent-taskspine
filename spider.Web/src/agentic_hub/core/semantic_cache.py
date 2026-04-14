"""Semantic caching — cache LLM responses by query similarity.

Uses mxbai-embed-large (via Ollama) for embeddings and Redis for storage.
If a new query is semantically similar (cosine > threshold) to a cached
query, returns the cached response instantly.

Cache entries: {query, response, agent, embedding, timestamp, hit_count}
In-memory index: list of (cache_key, embedding_vector) for fast lookup.
"""
from __future__ import annotations

import hashlib
import json
import logging
import math
import time
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_THRESHOLD = 0.88  # Lowered from 0.92 to increase cache hit rate (fewer model loads)
DEFAULT_TTL = 86400  # 24 hours
MAX_ENTRIES = 1000


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


class CacheEntry:
    """A cached query-response pair with its embedding."""

    def __init__(
        self,
        cache_key: str,
        query: str,
        response: str,
        agent: str,
        embedding: list[float],
        timestamp: float,
        hit_count: int = 0,
        tokens_in: int = 0,
        tokens_out: int = 0,
    ):
        self.cache_key = cache_key
        self.query = query
        self.response = response
        self.agent = agent
        self.embedding = embedding
        self.timestamp = timestamp
        self.hit_count = hit_count
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out

    def to_dict(self) -> dict:
        return {
            "query": self.query, "response": self.response, "agent": self.agent,
            "embedding": self.embedding, "timestamp": self.timestamp,
            "hit_count": self.hit_count, "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
        }

    @classmethod
    def from_dict(cls, key: str, d: dict) -> CacheEntry:
        return cls(
            cache_key=key, query=d["query"], response=d["response"],
            agent=d.get("agent", ""), embedding=d["embedding"],
            timestamp=d.get("timestamp", 0), hit_count=d.get("hit_count", 0),
            tokens_in=d.get("tokens_in", 0), tokens_out=d.get("tokens_out", 0),
        )


class SemanticCache:
    """Cache LLM responses keyed by semantic similarity of the query."""

    def __init__(
        self,
        threshold: float = DEFAULT_THRESHOLD,
        ttl: int = DEFAULT_TTL,
        max_entries: int = MAX_ENTRIES,
    ):
        self.threshold = threshold
        self.ttl = ttl
        self.max_entries = max_entries
        self._redis = None
        self._index: list[tuple[str, list[float]]] = []  # (cache_key, embedding)
        self._entries: dict[str, CacheEntry] = {}  # cache_key -> entry
        self._stats = {"hits": 0, "misses": 0, "tokens_saved": 0}

    async def connect_redis(self, url: str) -> None:
        """Connect to Redis and load existing cache into memory."""
        try:
            import redis.asyncio as aioredis
            self._redis = aioredis.from_url(url, decode_responses=True)
            await self._redis.ping()
            await self._load_from_redis()
            logger.info(f"Semantic cache: Redis connected, {len(self._index)} entries loaded")
        except Exception as e:
            logger.info(f"Semantic cache: running in-memory only ({e})")
            self._redis = None

    async def _load_from_redis(self) -> None:
        """Load all cached entries from Redis into the in-memory index."""
        if not self._redis:
            return
        try:
            keys = []
            async for key in self._redis.scan_iter("sem_cache:*"):
                keys.append(key)

            for key in keys[:self.max_entries]:
                raw = await self._redis.get(key)
                if raw:
                    data = json.loads(raw)
                    entry = CacheEntry.from_dict(key, data)
                    self._entries[key] = entry
                    self._index.append((key, entry.embedding))
        except Exception as e:
            logger.warning(f"Failed to load cache from Redis: {e}")

    async def _embed(self, text: str) -> list[float]:
        """Get embedding vector for text using Ollama mxbai-embed-large."""
        from agentic_hub.core.ollama_client import get_ollama
        ollama = get_ollama()
        # Truncate to avoid embedding huge texts
        text = text[:2000]
        embedding = await ollama.embed(text)
        return embedding

    async def get(self, query: str, agent: str = "") -> str | None:
        """Check cache for semantically similar query.

        Returns cached response or None.
        """
        if not self._index:
            self._stats["misses"] += 1
            return None

        try:
            query_embedding = await self._embed(query)
        except Exception:
            self._stats["misses"] += 1
            return None

        # Find nearest cached query
        best_key = None
        best_sim = 0.0

        for cache_key, cached_embedding in self._index:
            sim = _cosine_similarity(query_embedding, cached_embedding)
            if sim > best_sim:
                best_sim = sim
                best_key = cache_key

        if best_key and best_sim >= self.threshold:
            entry = self._entries.get(best_key)
            if entry is None:
                self._stats["misses"] += 1
                return None

            # Check TTL
            if time.time() - entry.timestamp > self.ttl:
                await self._evict(best_key)
                self._stats["misses"] += 1
                return None

            # Optional: filter by agent
            if agent and entry.agent and entry.agent != agent:
                self._stats["misses"] += 1
                return None

            # Cache hit
            entry.hit_count += 1
            self._stats["hits"] += 1
            self._stats["tokens_saved"] += entry.tokens_in + entry.tokens_out

            # Update hit count in Redis
            if self._redis:
                try:
                    data = entry.to_dict()
                    await self._redis.setex(best_key, self.ttl, json.dumps(data))
                except Exception:
                    pass

            logger.info(f"Cache HIT: sim={best_sim:.3f} query='{query[:50]}...'")
            return entry.response

        self._stats["misses"] += 1
        return None

    async def put(
        self,
        query: str,
        response: str,
        agent: str = "",
        tokens_in: int = 0,
        tokens_out: int = 0,
    ) -> None:
        """Cache a query-response pair."""
        if not response.strip():
            return

        try:
            embedding = await self._embed(query)
        except Exception:
            return

        # Generate cache key
        key_hash = hashlib.sha256(json.dumps(embedding[:8]).encode()).hexdigest()[:16]
        cache_key = f"sem_cache:{key_hash}"

        entry = CacheEntry(
            cache_key=cache_key, query=query, response=response, agent=agent,
            embedding=embedding, timestamp=time.time(),
            tokens_in=tokens_in, tokens_out=tokens_out,
        )

        # Evict oldest if at capacity
        if len(self._index) >= self.max_entries:
            oldest_key = min(self._entries, key=lambda k: self._entries[k].timestamp)
            await self._evict(oldest_key)

        self._entries[cache_key] = entry
        self._index.append((cache_key, embedding))

        # Persist to Redis
        if self._redis:
            try:
                await self._redis.setex(cache_key, self.ttl, json.dumps(entry.to_dict()))
            except Exception:
                pass

    async def _evict(self, cache_key: str) -> None:
        """Remove an entry from cache."""
        self._entries.pop(cache_key, None)
        self._index = [(k, e) for k, e in self._index if k != cache_key]
        if self._redis:
            try:
                await self._redis.delete(cache_key)
            except Exception:
                pass

    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        return {
            "entries": len(self._index),
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": round(self._stats["hits"] / total, 3) if total > 0 else 0,
            "tokens_saved": self._stats["tokens_saved"],
            "max_entries": self.max_entries,
            "threshold": self.threshold,
        }

    async def clear(self) -> None:
        """Clear all cached entries."""
        self._index.clear()
        self._entries.clear()
        if self._redis:
            try:
                async for key in self._redis.scan_iter("sem_cache:*"):
                    await self._redis.delete(key)
            except Exception:
                pass


# Singleton
_cache: SemanticCache | None = None


async def get_semantic_cache() -> SemanticCache:
    """Get or create the semantic cache singleton."""
    global _cache
    if _cache is None:
        from agentic_hub.config import get_settings
        settings = get_settings()

        _cache = SemanticCache(
            threshold=getattr(settings, "semantic_cache_threshold", DEFAULT_THRESHOLD),
            ttl=getattr(settings, "semantic_cache_ttl", DEFAULT_TTL),
        )

        if settings.redis_url:
            await _cache.connect_redis(settings.redis_url)

    return _cache
