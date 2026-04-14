# CDP CLI MCP Integration
Source: https://docs.cdp.coinbase.com/get-started/tools/cdp-cli-mcp

Use the CDP CLI as an MCP server to give AI agents typed tool access to every CDP API operation.

The `cdp mcp` command starts an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that exposes every CDP API operation as a typed tool. Any MCP-compatible agent can call these tools directly, with no manual API wiring needed.

Tools are generated dynamically from the embedded OpenAPI spec, so new endpoints appear automatically whenever the CLI updates. All tool names are prefixed with `cdp_` and mirror the nested resource structure using underscores (e.g. `cdp_evm_accounts_create`, `cdp_evm_accounts_sign_message`).

In addition to API tools, bundled skills walk agents through complete workflows like account creation, the encode-sign-send pipeline, and token swaps. Install them with `cdp skills add`.

## Setup

### Claude Code

**With the CLI installed globally:**

```bash theme={null}
claude mcp add --scope user --transport stdio cdp -- cdp mcp
```

**MCP only** (no global install needed, runs via `npx`):

```bash theme={null}
claude mcp add --scope user --transport stdio cdp -- npx -y @coinbase/cdp-cli mcp
```

<Info>
  When using both the CLI and MCP, install globally so they share the same version and spec.
</Info>

### Project-scoped setup

To enable the MCP server for a single project, add it to the project's `.mcp.json`:

```json theme={null}
{
  "mcpServers": {
    "cdp": { "transport": "stdio", "command": "cdp", "args": ["mcp"] }
  }
}
```

### Other MCP-compatible agents

Add the server to the agent's MCP configuration (format varies by agent):

```json theme={null}
{ "command": "cdp", "args": ["mcp"], "transport": "stdio" }
```

## Available tools

| Tool                      | Purpose                                 |
| ------------------------- | --------------------------------------- |
| `cdp_env`                 | Show active and configured environments |
| `cdp_set_env`             | Switch the active environment           |
| `cdp_help`                | Usage help for a resource or action     |
| `cdp_template`            | Request body template with examples     |
| `cdp_<resource>_<action>` | Execute an API operation                |

<Tip>
  Start any write operation with `cdp_template`. It returns the full request shape with field documentation and examples, which reduces back-and-forth guessing field names.
</Tip>

## Permissions

By default, Claude Code prompts before calling any MCP tool. To auto-approve read operations while requiring confirmation for writes, add the following to `.claude/settings.json`:

```json theme={null}
{
  "permissions": {
    "allow": [
      "mcp__cdp__cdp_env",
      "mcp__cdp__cdp_help",
      "mcp__cdp__cdp_template",
      "mcp__cdp__cdp_*_list",
      "mcp__cdp__cdp_*_get"
    ]
  }
}
```

This auto-approves `cdp_env`, `cdp_help`, `cdp_template`, `list`, and `get` operations. All mutating operations (`create`, `update`, `delete`, `sign`, `send`) still require confirmation.

