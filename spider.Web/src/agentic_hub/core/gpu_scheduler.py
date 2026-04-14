"""Single-GPU model loading coordinator.

Only one model fits in 8GB VRAM at a time. This module serializes
model swaps with an async lock and tracks which model is loaded.
"""
from __future__ import annotations

import asyncio
import logging

from agentic_hub.config import get_settings
from agentic_hub.core.ollama_client import get_ollama

logger = logging.getLogger(__name__)


class GPUScheduler:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._current_model: str | None = None
        self._keep_alive = get_settings().model_keep_alive

    @property
    def current_model(self) -> str | None:
        return self._current_model

    async def ensure_model(self, model_name: str) -> None:
        """Ensure the given model is loaded on the GPU. Thread-safe."""
        async with self._lock:
            if self._current_model == model_name:
                logger.debug(f"Model {model_name} already loaded")
                return

            ollama = get_ollama()

            # Unload current model if one is loaded
            if self._current_model:
                logger.info(f"Unloading {self._current_model} from GPU")
                await ollama.unload_model(self._current_model)

            # Warm-load the new model
            logger.info(f"Loading {model_name} onto GPU")
            await ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": "hi"}],
                keep_alive=self._keep_alive,
            )
            self._current_model = model_name
            logger.info(f"Model {model_name} loaded and ready")

    async def get_status(self) -> dict:
        """Return current GPU scheduler state."""
        ollama = get_ollama()
        running = await ollama.get_running_models()
        return {
            "tracked_model": self._current_model,
            "running_models": [m.get("name", "unknown") for m in running],
            "lock_held": self._lock.locked(),
        }


# Singleton
_scheduler: GPUScheduler | None = None


def get_gpu_scheduler() -> GPUScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = GPUScheduler()
    return _scheduler
