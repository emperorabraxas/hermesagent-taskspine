# Freshdesk → Claude Code Integration

Automatically injects support tickets into your Claude Code session with plans and Freshdesk links.

## Quick Setup

1. **Create Freshdesk account** at [freshdesk.com](https://freshdesk.com) (free tier)

2. **Get your API key:** Freshdesk → Profile Settings → API Key

3. **Configure:**
   ```bash
   cd freshdesk-integration
   cp .env.example .env
   # Add: FRESHDESK_DOMAIN=yourcompany.freshdesk.com
   # Add: FRESHDESK_API_KEY=your_key
   npm install
   ```

4. **Add MCP server to Claude Code** (`~/.claude/settings.json`):
   ```json
   {
     "mcpServers": {
       "freshdesk": {
         "command": "node",
         "args": ["mcp-server/index.js"],
         "cwd": "/home/user/hermesagent-taskspine/freshdesk-integration"
       }
     }
   }
   ```

5. **Enable auto-polling in your session:**
   ```
   /loop 5m check for new Freshdesk tickets and show me any with their plans + links
   ```

## What Happens

When a ticket comes in, Claude will automatically:
- Show ticket details (subject, priority, description)
- Generate a plan (bug fix, how-to, feature request, etc.)
- Post the Freshdesk link: `https://yourcompany.freshdesk.com/a/tickets/123`

You click the link, handle it, done.

## Manual Commands

In your Claude Code session, just ask:
- "Check my tickets"
- "Get ticket #123"
- "Reply to ticket #456 with [message]"
- "What's urgent?"

## Background Service (Optional)

For 24/7 monitoring with Slack notifications:
```bash
# Install service
cp freshdesk-handler.service ~/.config/systemd/user/
systemctl --user enable freshdesk-handler
systemctl --user start freshdesk-handler
```

Add `SLACK_WEBHOOK_URL` to `.env` for Slack notifications.

## MCP Tools

| Tool | Description |
|------|-------------|
| `list_tickets` | List recent tickets |
| `get_ticket` | Get full ticket + conversation |
| `reply_to_ticket` | Send reply to customer |
| `add_private_note` | Internal note (hidden from customer) |
| `update_ticket_status` | Change status/priority |
| `get_new_tickets` | Tickets from last N minutes |
