"""MCP Server — expose spider.Web tools as an MCP server.

External clients (Claude Desktop, other MCP clients) can discover
and call spider.Web's tools through the standard MCP protocol.

Usage:
    # As stdio server (for Claude Desktop config)
    python -m agentic_hub.core.mcp.server

    # Programmatic
    from agentic_hub.core.mcp.server import create_mcp_server
    server = create_mcp_server()
    await server.run_stdio()
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def create_mcp_server():
    """Create an MCP server exposing spider.Web's tools.

    Returns a configured MCP Server ready to run.
    """
    from mcp.server import Server
    from mcp.types import TextContent, Tool

    server = Server("spider.web")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List all spider.Web tools as MCP tools."""
        from agentic_hub.core.tools.registry import get_registry
        registry = get_registry()
        tools = []
        for tool in registry.get_all_tools():
            schema = tool.to_json_schema()
            func_def = schema.get("function", {})
            tools.append(Tool(
                name=tool.name,
                description=tool.description,
                inputSchema=func_def.get("parameters", {}),
            ))
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Execute a spider.Web tool via MCP."""
        from agentic_hub.core.tools.registry import get_registry
        registry = get_registry()
        tool = registry.get_tool(name)
        if tool is None:
            return [TextContent(type="text", text=f"Tool '{name}' not found")]

        result = await tool.execute(**arguments)
        output = result.output if result.success else f"Error: {result.error}"
        return [TextContent(type="text", text=output)]

    return server


async def run_stdio_server():
    """Run the MCP server with stdio transport."""
    from mcp.server.stdio import stdio_server

    server = create_mcp_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


# Allow running as a module: python -m agentic_hub.core.mcp.server
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_stdio_server())
