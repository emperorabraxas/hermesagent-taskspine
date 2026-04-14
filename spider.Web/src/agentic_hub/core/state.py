"""State bus — in-memory pub/sub state store replacing disk-file IPC.

Replaces the pattern where idle_daemon and market_daemon write JSON files to disk
and other components read them. Now all state flows through a centralized store
with optional Redis persistence and pub/sub notifications.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, Callable, Awaitable

logger = logging.getLogger(__name__)


class StateStore:
    """In-memory state store with pub/sub and optional Redis backing.

    Keys use dot-notation for namespacing:
        "market_intel.latest"
        "idle_research.scholar"
        "agent.oracle.last_output"
        "pipeline.code.status"
    """

    def __init__(self):
        self._state: dict[str, Any] = {}
        self._timestamps: dict[str, float] = {}
        self._subscribers: dict[str, list[Callable]] = {}  # pattern -> callbacks
        self._redis = None

    async def connect_redis(self, url: str = "redis://localhost:6380"):
        """Optional Redis backing for persistence across restarts."""
        try:
            import redis.asyncio as aioredis
            self._redis = aioredis.from_url(url, decode_responses=True)
            await self._redis.ping()
            logger.info("State bus connected to Redis")
        except Exception as e:
            logger.info(f"State bus running in-memory only (Redis unavailable: {e})")
            self._redis = None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set a value in the state store."""
        self._state[key] = value
        self._timestamps[key] = time.time()

        # Persist to Redis if available
        if self._redis:
            try:
                serialized = json.dumps(value, default=str)
                if ttl:
                    await self._redis.setex(f"sw:{key}", ttl, serialized)
                else:
                    await self._redis.set(f"sw:{key}", serialized)
            except Exception:
                pass

        # Notify subscribers
        await self._notify(key, value)

    async def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state store."""
        if key in self._state:
            return self._state[key]

        # Try Redis fallback
        if self._redis:
            try:
                val = await self._redis.get(f"sw:{key}")
                if val:
                    parsed = json.loads(val)
                    self._state[key] = parsed
                    return parsed
            except Exception:
                pass

        return default

    async def get_with_age(self, key: str) -> tuple[Any, float]:
        """Get a value and its age in seconds. Returns (None, inf) if not found."""
        value = await self.get(key)
        if value is None:
            return None, float("inf")
        age = time.time() - self._timestamps.get(key, 0)
        return value, age

    async def delete(self, key: str) -> None:
        """Remove a key from the store."""
        self._state.pop(key, None)
        self._timestamps.pop(key, None)
        if self._redis:
            try:
                await self._redis.delete(f"sw:{key}")
            except Exception:
                pass

    def subscribe(self, pattern: str, callback: Callable[[str, Any], Awaitable[None]]) -> None:
        """Subscribe to state changes matching a key pattern.

        Pattern supports simple prefix matching with '*':
            "market_intel.*" — matches any market_intel key
            "agent.*" — matches any agent key
            "pipeline.code.status" — exact match
        """
        if pattern not in self._subscribers:
            self._subscribers[pattern] = []
        self._subscribers[pattern].append(callback)

    async def _notify(self, key: str, value: Any) -> None:
        """Notify all matching subscribers."""
        for pattern, callbacks in self._subscribers.items():
            if self._matches(pattern, key):
                for cb in callbacks:
                    try:
                        await cb(key, value)
                    except Exception as e:
                        logger.warning(f"State subscriber error for {pattern}: {e}")

    @staticmethod
    def _matches(pattern: str, key: str) -> bool:
        """Check if a key matches a subscription pattern."""
        if pattern == key:
            return True
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            return key.startswith(prefix)
        return False

    def keys(self, prefix: str = "") -> list[str]:
        """List all keys, optionally filtered by prefix."""
        if not prefix:
            return list(self._state.keys())
        return [k for k in self._state if k.startswith(prefix)]

    def snapshot(self) -> dict[str, Any]:
        """Get a snapshot of all state (for debugging/API)."""
        return {
            k: {"value": v, "age_s": round(time.time() - self._timestamps.get(k, 0), 1)}
            for k, v in self._state.items()
        }


# Singleton
_store: StateStore | None = None


def get_state_store() -> StateStore:
    global _store
    if _store is None:
        _store = StateStore()
    return _store
