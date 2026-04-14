"""MCP Client — discover and connect to external MCP tool servers.

Connects to MCP servers defined in models.yaml, discovers their tools,
and registers them as BaseTool instances in the spider.Web ToolRegistry.

Config format in models.yaml:
    mcp_servers:
      - name: filesystem
        command: npx
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"]
      - name: github
        command: npx
        args: ["-y", "@modelcontextprotocol/server-github"]
        env:
          GITHUB_TOKEN: "${GITHUB_TOKEN}"
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class MCPClientManager:
    """Manage connections to external MCP servers."""

    def __init__(self):
        self._sessions: dict[str, Any] = {}  # name -> (client, session)
        self._connected: set[str] = set()

    async def discover_and_connect(self) -> int:
        """Discover MCP servers from config and connect to them.

        Returns count of tools registered.
        """
        from agentic_hub.config import load_models_config

        config = load_models_config()
        servers = config.get("mcp_servers", [])
        if not servers:
            logger.info("No MCP servers configured in models.yaml")
            return 0

        total_tools = 0
        for server_config in servers:
            name = server_config.get("name", "unknown")
            try:
                count = await self._connect_server(name, server_config)
                total_tools += count
                logger.info(f"MCP server '{name}': {count} tools registered")
            except Exception as e:
                logger.warning(f"MCP server '{name}' failed: {e}")

        return total_tools

    async def _connect_server(self, name: str, config: dict) -> int:
        """Connect to a single MCP server and register its tools."""
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        command = config.get("command", "")
        args = config.get("args", [])
        env_overrides = config.get("env", {})

        if not command:
            logger.warning(f"MCP server '{name}' has no command")
            return 0

        # Build environment with overrides
        env = dict(os.environ)
        for k, v in env_overrides.items():
            # Expand ${VAR} references
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                env_var = v[2:-1]
                env[k] = os.environ.get(env_var, "")
            else:
                env[k] = str(v)

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env,
        )

        # Connect via stdio transport
        read_stream, write_stream = await stdio_client(server_params).__aenter__()
        session = ClientSession(read_stream, write_stream)
        await session.__aenter__()
        await session.initialize()

        self._sessions[name] = session
        self._connected.add(name)

        # Discover tools
        tools_response = await session.list_tools()
        tools = tools_response.tools if hasattr(tools_response, 'tools') else []

        # Register each tool in spider.Web's registry
        from agentic_hub.core.tools.registry import get_registry
        from agentic_hub.core.mcp.adapter import MCPToolAdapter

        registry = get_registry()
        for tool in tools:
            tool_def = {
                "name": tool.name,
                "description": tool.description or "",
                "inputSchema": tool.inputSchema if hasattr(tool, 'inputSchema') else {},
            }

            async def _make_call_fn(sess, tool_name):
                async def call_tool(name: str, args: dict) -> str:
                    result = await sess.call_tool(name, arguments=args)
                    # Extract text content from result
                    if hasattr(result, 'content'):
                        parts = []
                        for content in result.content:
                            if hasattr(content, 'text'):
                                parts.append(content.text)
                        return "\n".join(parts) if parts else str(result)
                    return str(result)
                return call_tool

            call_fn = await _make_call_fn(session, tool.name)
            adapter = MCPToolAdapter(tool_def, call_fn)
            registry.register(adapter)

        return len(tools)

    async def disconnect_all(self) -> None:
        """Disconnect from all MCP servers."""
        for name, session in self._sessions.items():
            try:
                await session.__aexit__(None, None, None)
                logger.info(f"MCP server '{name}' disconnected")
            except Exception:
                pass
        self._sessions.clear()
        self._connected.clear()

    @property
    def connected_servers(self) -> list[str]:
        return list(self._connected)


# Singleton
_client: MCPClientManager | None = None


def get_mcp_client() -> MCPClientManager:
    global _client
    if _client is None:
        _client = MCPClientManager()
    return _client
