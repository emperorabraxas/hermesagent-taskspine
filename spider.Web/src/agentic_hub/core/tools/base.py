"""Tool base class — every tool is a schema-defined callable the LLM selects."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolParameter:
    """One parameter of a tool, maps to JSON Schema property."""
    name: str
    type: str           # "string", "integer", "number", "boolean", "array", "object"
    description: str
    required: bool = True
    enum: list[str] | None = None
    default: Any = None


@dataclass
class ToolResult:
    """Structured result from a tool execution."""
    output: str
    success: bool
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)  # latency_ms, bytes_read, etc.


class BaseTool(ABC):
    """Abstract base for all tools. Subclass and implement name/description/parameters/execute."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (snake_case), e.g. 'shell', 'read_file'."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """What this tool does — injected into LLM prompt for tool selection."""
        ...

    @property
    @abstractmethod
    def parameters(self) -> list[ToolParameter]:
        """Ordered list of parameters the tool accepts."""
        ...

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Run the tool with validated kwargs. Must not raise — return ToolResult with error."""
        ...

    def to_json_schema(self) -> dict:
        """Generate OpenAI-compatible function schema (also used by Ollama, xAI, DeepSeek)."""
        properties = {}
        required = []
        for p in self.parameters:
            prop: dict[str, Any] = {"type": p.type, "description": p.description}
            if p.enum:
                prop["enum"] = p.enum
            if p.default is not None:
                prop["default"] = p.default
            properties[p.name] = prop
            if p.required:
                required.append(p.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }

    def to_anthropic_schema(self) -> dict:
        """Generate Anthropic tool_use schema (slightly different format)."""
        schema = self.to_json_schema()["function"]
        return {
            "name": schema["name"],
            "description": schema["description"],
            "input_schema": schema["parameters"],
        }

    def __repr__(self) -> str:
        return f"<Tool:{self.name}>"
