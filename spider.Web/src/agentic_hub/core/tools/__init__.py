"""spider.Web tool system — schema-defined tools that LLMs select and invoke."""
from agentic_hub.core.tools.base import BaseTool, ToolParameter, ToolResult
from agentic_hub.core.tools.registry import ToolRegistry, get_registry

__all__ = ["BaseTool", "ToolParameter", "ToolResult", "ToolRegistry", "get_registry"]
