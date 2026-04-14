"""Structured LLM response — unified format for tool calling across all providers."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ToolCall:
    """A single tool call requested by the LLM."""
    name: str
    arguments: dict
    call_id: str = ""  # Provider-assigned ID (needed for Anthropic/OpenAI response pairing)


@dataclass
class LLMResponse:
    """Unified response from any LLM provider, with optional tool calls and metadata."""
    text: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    thinking: str = ""
    tokens_in: int = 0
    tokens_out: int = 0
    model: str = ""
    provider: str = ""

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0
