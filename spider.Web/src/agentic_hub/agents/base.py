"""Base agent interface for local model agents."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator


@dataclass
class AgentInfo:
    name: str
    display_name: str
    description: str
    local_model: str
    xp_base: int
    source: str = "local"


class BaseAgent(ABC):
    """Abstract base for agents that run on local models via Ollama."""

    @property
    @abstractmethod
    def info(self) -> AgentInfo:
        ...

    @abstractmethod
    async def process(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
        stream: bool = True,
    ) -> str | AsyncIterator[str]:
        """Process a message. Returns full text or streams chunks."""
        ...
