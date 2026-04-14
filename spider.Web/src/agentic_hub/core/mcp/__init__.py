"""MCP integration — Model Context Protocol server + client.

spider.Web as MCP server: exposes its tools to external clients.
spider.Web as MCP client: discovers and consumes external MCP tool servers.
"""
from agentic_hub.core.mcp.adapter import MCPToolAdapter
from agentic_hub.core.mcp.client import MCPClientManager, get_mcp_client
from agentic_hub.core.mcp.server import create_mcp_server

__all__ = ["MCPToolAdapter", "MCPClientManager", "get_mcp_client", "create_mcp_server"]
