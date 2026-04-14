"""Error resilience — retry with backoff, circuit breaker, cancellation."""
from __future__ import annotations

import asyncio
import logging
import random
import time
from typing import Any, Callable, TypeVar

import httpx

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Default retryable exceptions
RETRYABLE_EXCEPTIONS = (
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
    ConnectionError,
    TimeoutError,
    OSError,
)


async def retry_with_backoff(
    fn: Callable[..., Any],
    *args: Any,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: bool = True,
    retryable: tuple = RETRYABLE_EXCEPTIONS,
    **kwargs: Any,
) -> Any:
    """Execute an async function with exponential backoff on transient failures.

    Args:
        fn: Async function to call.
        max_retries: Maximum retry attempts (0 = no retries).
        base_delay: Initial delay in seconds.
        max_delay: Maximum delay cap.
        jitter: Add random jitter to prevent thundering herd.
        retryable: Tuple of exception types to retry on.
    """
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return await fn(*args, **kwargs)
        except retryable as e:
            last_error = e
            if attempt == max_retries:
                logger.warning(f"Retry exhausted after {max_retries + 1} attempts: {e}")
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            if jitter:
                delay *= (0.5 + random.random())  # 50%-150% of calculated delay
            logger.info(f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s: {e}")
            await asyncio.sleep(delay)
    raise last_error  # Should never reach here


class CircuitBreaker:
    """Per-provider circuit breaker.

    After FAILURE_THRESHOLD consecutive failures, the circuit opens and
    skips the provider for RECOVERY_TIME seconds. After recovery, it
    half-opens (allows one attempt) to test if the provider is back.

    Usage:
        breaker = get_circuit_breaker()
        if breaker.is_open("anthropic"):
            # Skip this provider, use fallback
        try:
            result = await client.chat(...)
            breaker.record_success("anthropic")
        except Exception:
            breaker.record_failure("anthropic")
    """
    FAILURE_THRESHOLD = 3
    RECOVERY_TIME = 60  # seconds

    def __init__(self):
        self._failures: dict[str, int] = {}
        self._open_until: dict[str, float] = {}
        self._last_failure_time: dict[str, float] = {}

    def is_open(self, provider: str) -> bool:
        """Check if the circuit is open (provider should be skipped)."""
        open_until = self._open_until.get(provider, 0)
        if open_until == 0:
            return False
        if time.time() >= open_until:
            # Recovery period expired — half-open (allow one attempt)
            return False
        return True

    def record_failure(self, provider: str) -> None:
        """Record a failure. Opens circuit after threshold."""
        self._failures[provider] = self._failures.get(provider, 0) + 1
        self._last_failure_time[provider] = time.time()
        if self._failures[provider] >= self.FAILURE_THRESHOLD:
            self._open_until[provider] = time.time() + self.RECOVERY_TIME
            logger.warning(
                f"Circuit OPEN for {provider}: {self._failures[provider]} consecutive failures. "
                f"Skipping for {self.RECOVERY_TIME}s."
            )

    def record_success(self, provider: str) -> None:
        """Record a success. Resets failure count and closes circuit."""
        if provider in self._failures:
            was_open = self._open_until.get(provider, 0) > 0
            self._failures[provider] = 0
            self._open_until[provider] = 0
            if was_open:
                logger.info(f"Circuit CLOSED for {provider}: recovered")

    def get_status(self) -> dict[str, str]:
        """Get circuit status for all tracked providers."""
        now = time.time()
        status = {}
        for provider in set(list(self._failures.keys()) + list(self._open_until.keys())):
            open_until = self._open_until.get(provider, 0)
            failures = self._failures.get(provider, 0)
            if open_until > now:
                status[provider] = f"OPEN (resets in {int(open_until - now)}s, {failures} failures)"
            elif failures > 0:
                status[provider] = f"HALF-OPEN ({failures} recent failures)"
            else:
                status[provider] = "CLOSED"
        return status


# Singleton
_breaker: CircuitBreaker | None = None


def get_circuit_breaker() -> CircuitBreaker:
    global _breaker
    if _breaker is None:
        _breaker = CircuitBreaker()
    return _breaker
