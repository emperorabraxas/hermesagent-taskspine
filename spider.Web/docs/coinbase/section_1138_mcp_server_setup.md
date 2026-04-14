# MCP Server Setup
Source: https://docs.cdp.coinbase.com/get-started/develop-with-ai/setup/ai-mcp-setup

Connect AI tools to CDP documentation using the Model Context Protocol for enhanced development assistance

## Overview

Think of MCP (Model Context Protocol) as giving your AI assistant a direct hotline to Coinbase's documentation. Instead of the AI guessing how CDP works, it can instantly look up the correct way to build apps.

**Without MCP:**

```
You: "Create a wallet connection component"
AI: *generates generic code that might not work with CDP*
```

**With MCP:**

```
You: "Create a wallet connection component" 
AI: *searches CDP docs automatically*
AI: *generates code using actual CDP components*
```

## How it helps you

When you connect MCP to your AI tools, the AI becomes a CDP expert that can:

* **Generate accurate code** using our latest components
* **Answer specific questions** about CDP APIs and authentication
* **Suggest best practices** for embedded wallets, payments, and transactions
* **Find the right documentation** when you're stuck on implementation

<Note>
  The CDP MCP server currently provides documentation `search`. It doesn't execute API calls directly - that keeps your development secure.
</Note>

## Claude

To use the CDP MCP server with Claude:

<Steps>
  <Step title="Add the CDP MCP server to Claude">
    1. Navigate to the [Connectors](https://claude.ai/settings/connectors) page in Claude settings
    2. Select **Add custom connector**
    3. Add the following:
       * Name: `Coinbase Developer Platform`
       * URL: `https://docs.cdp.coinbase.com/mcp`
    4. Select **Add**
  </Step>

  <Step title="Access CDP docs in your chat">
    1. When using Claude, select the attachments button (the plus icon)
    2. Select the Coinbase Developer Platform connector
    3. Query Claude with CDP documentation as context
  </Step>
</Steps>

## Cursor

To connect the CDP MCP server to Cursor, you can either use the automatic connection or configure it manually:

<Tabs>
  <Tab title="Automatic Connection">
    <Steps>
      <Step title="Use the Connect to Cursor option">
        1. On any CDP documentation page, select the **Copy page** dropdown next to the document header
        2. Select **Connect to Cursor**
        3. Cursor will automatically open with the CDP MCP server configured
      </Step>

      <Step title="Test the connection">
        In Cursor's chat, ask "What tools do you have available?" to verify that Cursor has access to CDP documentation search and any configured API endpoints.
      </Step>
    </Steps>
  </Tab>

  <Tab title="Manual Configuration">
    <Steps>
      <Step title="Open MCP settings">
        1. Use <kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> on Windows) to open the command palette
        2. Search for "Open MCP settings"
        3. Select **Open MCP settings** to open the `mcp.json` file
      </Step>

      <Step title="Configure the CDP server">
        In `mcp.json`, add the CDP configuration:

        ```json theme={null}
        {
          "mcpServers": {
            "coinbase-cdp": {
              "url": "https://docs.cdp.coinbase.com/mcp"
            }
          }
        }
        ```
      </Step>

      <Step title="Test the connection">
        In Cursor's chat, ask "Do you have access to an MCP server?" to verify that Cursor has access to CDP documentation search and any configured API endpoints.
      </Step>
    </Steps>
  </Tab>
</Tabs>

## VS Code

The CDP MCP server can also be configured with VS Code extensions that support MCP:

1. Install an MCP-compatible extension
2. Add the CDP server URL: `https://docs.cdp.coinbase.com/mcp`
3. Test the connection by querying CDP documentation

<Note>
  VS Code MCP support varies by extension. Check your specific extension's documentation for setup instructions.
</Note>

## Testing your MCP connection

Once configured, test your MCP connection by asking your AI tool:

```
"What MCP tools do you have available?"
```

You should see the CDP documentation search tool listed. Then try:

```
"Search for information about embedded wallets in the CDP documentation"
```

The AI should be able to search and return relevant CDP documentation.

## Troubleshooting

### Connection issues

**Problem:** MCP server not connecting

**Solution:**

* Verify the URL is exactly: `https://docs.cdp.coinbase.com/mcp`
* Check your internet connection
* Restart your AI tool after configuration

**Problem:** Search tool not available

**Solution:**

* Confirm the MCP server was added correctly
* Try removing and re-adding the server configuration
* Check the AI tool's MCP support documentation

### Search issues

**Problem:** Search returns no results
**Solution:**

* Try different search terms
* Use more general terms (e.g., "wallet" instead of "embedded wallet API")
* Verify the MCP connection is working

## Additional resources

* [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/tutorials/use-remote-mcp-server#connecting-to-a-remote-mcp-server)
* [Mintlify MCP documentation](https://mintlify.com/docs/ai/model-context-protocol)

## What to read next

With MCP configured, your AI tools now have direct access to CDP documentation. Continue with:

* **[AI Development Setup](/get-started/develop-with-ai/setup/ai-development-setup)**: Configure your starter app and development environment for optimal AI-assisted development
* **[AI Development Workflows](/get-started/develop-with-ai/development/develop-with-ai-workflows)**: Learn day-to-day development practices and core workflow patterns
* **[AI Prompting Techniques](/get-started/develop-with-ai/development/ai-prompting-techniques)**: Master effective prompting patterns to leverage your new MCP connection

