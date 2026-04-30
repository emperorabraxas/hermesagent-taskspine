# Freshdesk → Claude Code Integration

Integrates Freshdesk support tickets directly with your Claude Code terminal session.

## Setup

1. **Create Freshdesk account** at [freshdesk.com](https://freshdesk.com) (free tier works)

2. **Get your API key:**
   - Freshdesk → Profile Settings → API Key

3. **Configure environment:**
   ```bash
   cd freshdesk-integration
   cp .env.example .env
   # Edit .env with your domain and API key
   ```

4. **Install dependencies:**
   ```bash
   npm install
   ```

## Usage

### Option 1: Polling Daemon (Push-based)

Run in a separate terminal — tickets appear automatically:

```bash
npm run poll
```

When a new/updated ticket arrives, you'll see a notification with:
- Ticket details
- Suggested plan
- Command to handle it

Then run:
```bash
npm run plan -- <ticket_id>          # Show the plan
npm run plan -- <ticket_id> execute  # Launch Claude Code with context
```

### Option 2: MCP Server (Pull-based)

Add to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "freshdesk": {
      "command": "node",
      "args": ["mcp-server/index.js"],
      "cwd": "/path/to/freshdesk-integration"
    }
  }
}
```

Then in Claude Code, you can ask:
- "List my open tickets"
- "Get ticket #123"
- "Reply to ticket #456 with..."
- "What's urgent in my queue?"

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_tickets` | List recent tickets |
| `get_ticket` | Get full ticket with conversation history |
| `add_private_note` | Add internal note (not visible to customer) |
| `reply_to_ticket` | Send reply to customer |
| `update_ticket_status` | Change status/priority |
| `get_new_tickets` | Get recently updated tickets |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FRESHDESK_DOMAIN` | Your Freshdesk domain (e.g., `yourcompany.freshdesk.com`) |
| `FRESHDESK_API_KEY` | Your API key from profile settings |
| `POLL_INTERVAL_MS` | Polling interval in ms (default: 30000) |
| `CLAUDE_SESSION_FILE` | Queue file path (default: `/tmp/claude-ticket-queue.json`) |
| `NOTIFY_SOUND` | Play sound on new tickets (default: false) |
