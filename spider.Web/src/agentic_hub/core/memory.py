"""Conversation memory backed by Redis + in-memory fallback."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Message:
    role: str       # "user", "assistant", "system"
    content: str
    agent: str = ""
    model: str = ""
    source: str = ""  # "local" or "cloud"


class ConversationMemory:
    """Manages conversation history for a session.

    Stores messages in-memory with optional Redis persistence.
    Redis is best-effort — works without it.
    """

    def __init__(self, conversation_id: str, max_messages: int = 50):
        self.conversation_id = conversation_id
        self.max_messages = max_messages
        self._messages: list[Message] = []
        self._redis = None

    async def connect_redis(self, redis_url: str) -> None:
        """Optionally connect to Redis for persistence."""
        try:
            import redis.asyncio as aioredis
            self._redis = aioredis.from_url(redis_url, decode_responses=True)
            await self._redis.ping()
            # Load existing messages
            stored = await self._redis.lrange(f"conv:{self.conversation_id}", 0, -1)
            self._messages = [Message(**json.loads(m)) for m in stored]
            logger.info(f"Redis connected, loaded {len(self._messages)} messages")
        except Exception as e:
            logger.warning(f"Redis unavailable, using in-memory only: {e}")
            self._redis = None

    async def add(self, message: Message) -> None:
        """Add a message to the conversation."""
        self._messages.append(message)
        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]

        if self._redis:
            try:
                await self._redis.rpush(
                    f"conv:{self.conversation_id}",
                    json.dumps(message.__dict__),
                )
                await self._redis.ltrim(
                    f"conv:{self.conversation_id}",
                    -self.max_messages, -1,
                )
                await self._redis.expire(f"conv:{self.conversation_id}", 3600)
            except Exception as e:
                logger.warning(f"Redis write failed: {e}")

    def get_history(self, last_n: int | None = None) -> list[dict]:
        """Get conversation history as list of dicts for API calls."""
        msgs = self._messages if last_n is None else self._messages[-last_n:]
        return [{"role": m.role, "content": m.content} for m in msgs]

    def get_full_history(self) -> list[Message]:
        """Get full message objects with metadata."""
        return list(self._messages)

    async def clear(self) -> None:
        """Clear conversation history."""
        self._messages.clear()
        if self._redis:
            try:
                await self._redis.delete(f"conv:{self.conversation_id}")
            except Exception:
                pass
