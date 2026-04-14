"""MCP Tool Adapter — wraps external MCP tools as spider.Web BaseTool instances.

This allows MCP-discovered tools to be used by spider.Web agents through
the existing ToolRegistry with zero changes to the tool-calling loop.
"""
from __future__ import annotations

import logging
from typing import Any

from agentic_hub.core.tools.base import BaseTool, ToolParameter, ToolResult

logger = logging.getLogger(__name__)


class MCPToolAdapter(BaseTool):
    """Wraps an external MCP tool as a spider.Web BaseTool.

    Converts MCP tool definitions (JSON schema) into ToolParameter lists,
    and routes execute() calls through the MCP client.
    """

    def __init__(self, tool_def: dict, call_fn):
        """
        Args:
            tool_def: MCP tool definition with name, description, inputSchema.
            call_fn: Async function to call the MCP tool: async (name, args) -> str
        """
        self._def = tool_def
        self._call_fn = call_fn
        self._name = f"mcp_{tool_def.get('name', 'unknown')}"
        self._description = tool_def.get("description", "External MCP tool")
        self._params = self._parse_params(tool_def.get("inputSchema", {}))

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def parameters(self) -> list[ToolParameter]:
        return self._params

    async def execute(self, **kwargs: Any) -> ToolResult:
        try:
            # Call the MCP tool via the client
            original_name = self._def.get("name", self._name.removeprefix("mcp_"))
            result = await self._call_fn(original_name, kwargs)
            return ToolResult(output=str(result), success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"MCP tool error: {e}")

    @staticmethod
    def _parse_params(schema: dict) -> list[ToolParameter]:
        """Convert JSON Schema properties to ToolParameter list."""
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        params = []
        for name, prop in props.items():
            params.append(ToolParameter(
                name=name,
                type=prop.get("type", "string"),
                description=prop.get("description", ""),
                required=name in required,
                enum=prop.get("enum"),
                default=prop.get("default"),
            ))
        return params
