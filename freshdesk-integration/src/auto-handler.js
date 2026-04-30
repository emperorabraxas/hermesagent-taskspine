#!/usr/bin/env node
import 'dotenv/config';
import { FreshdeskClient } from './freshdesk-client.js';
import chalk from 'chalk';
import { spawn, execSync } from 'child_process';
import axios from 'axios';

const POLL_INTERVAL = parseInt(process.env.POLL_INTERVAL_MS || '30000', 10);
const SLACK_WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL;
const seenTickets = new Map();

async function main() {
  const domain = process.env.FRESHDESK_DOMAIN;
  const apiKey = process.env.FRESHDESK_API_KEY;

  if (!domain || !apiKey) {
    console.error(chalk.red('Missing FRESHDESK_DOMAIN or FRESHDESK_API_KEY in .env'));
    process.exit(1);
  }

  const client = new FreshdeskClient(domain, apiKey);

  console.log(chalk.cyan('🤖 Freshdesk Auto-Handler Running'));
  console.log(chalk.gray(`Polling ${domain} every ${POLL_INTERVAL / 1000}s`));
  console.log(chalk.gray(`Slack notifications: ${SLACK_WEBHOOK_URL ? 'enabled' : 'disabled'}\n`));

  async function poll() {
    try {
      const tickets = await client.getNewOrUpdatedTickets(5);

      for (const ticket of tickets) {
        const lastSeen = seenTickets.get(ticket.id);
        const ticketUpdated = new Date(ticket.updated_at).getTime();

        if (!lastSeen || ticketUpdated > lastSeen) {
          seenTickets.set(ticket.id, ticketUpdated);

          const fullTicket = await client.getTicket(ticket.id);
          const formatted = client.formatTicketForClaude(fullTicket);
          const isNew = !lastSeen;

          console.log(chalk.yellow(`\n🎫 ${isNew ? 'New' : 'Updated'} Ticket #${ticket.id}: ${formatted.subject}`));

          // Generate the plan and Claude prompt
          const claudePrompt = generateClaudePrompt(formatted);
          const plan = generatePlan(formatted);

          // Post to Slack with link
          if (SLACK_WEBHOOK_URL) {
            await postToSlack(formatted, plan, isNew);
          }

          // Auto-spawn Claude Code session
          spawnClaudeSession(formatted, claudePrompt);
        }
      }
    } catch (error) {
      if (error.response?.status === 401) {
        console.error(chalk.red('Auth failed. Check API key.'));
        process.exit(1);
      }
      console.error(chalk.red(`Poll error: ${error.message}`));
    }
  }

  await poll();
  setInterval(poll, POLL_INTERVAL);

  process.on('SIGINT', () => {
    console.log(chalk.cyan('\nShutting down...'));
    process.exit(0);
  });
}

function generatePlan(ticket) {
  const steps = [];
  const desc = ticket.description.toLowerCase();

  if (desc.includes('error') || desc.includes('bug') || desc.includes('broken')) {
    steps.push('🔍 Identify error and affected component');
    steps.push('🔧 Implement fix');
    steps.push('✉️ Draft resolution response');
  } else if (desc.includes('how to') || desc.includes('help') || desc.includes('question')) {
    steps.push('📖 Research answer');
    steps.push('✉️ Draft step-by-step response');
  } else if (desc.includes('feature') || desc.includes('request')) {
    steps.push('📝 Document request');
    steps.push('✉️ Draft response with timeline');
  } else {
    steps.push('🔍 Analyze ticket');
    steps.push('✉️ Draft response');
  }

  return steps;
}

function generateClaudePrompt(ticket) {
  const conversations = ticket.conversations.length > 0
    ? ticket.conversations.map(c => `[${c.incoming ? 'Customer' : 'Support'}] ${c.body.slice(0, 500)}`).join('\n\n')
    : 'No previous replies.';

  return `## Support Ticket #${ticket.id}

**Subject:** ${ticket.subject}
**From:** ${ticket.requester} <${ticket.requesterEmail || 'unknown'}>
**Priority:** ${ticket.priority} | **Status:** ${ticket.status}

### Description
${ticket.description}

### Conversation History
${conversations}

---

Analyze this ticket and help me:
1. Understand the core issue
2. Draft a helpful response
3. If code changes needed, identify files and changes`;
}

async function postToSlack(ticket, plan, isNew) {
  const emoji = isNew ? '🆕' : '🔄';
  const priorityEmoji = ticket.priority === 'Urgent' ? '🔴' :
                        ticket.priority === 'High' ? '🟠' :
                        ticket.priority === 'Medium' ? '🟡' : '🟢';

  const message = {
    blocks: [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `${emoji} ${isNew ? 'New' : 'Updated'} Ticket #${ticket.id}`,
          emoji: true
        }
      },
      {
        type: 'section',
        fields: [
          { type: 'mrkdwn', text: `*Subject:*\n${ticket.subject}` },
          { type: 'mrkdwn', text: `*From:*\n${ticket.requester}` },
          { type: 'mrkdwn', text: `*Priority:*\n${priorityEmoji} ${ticket.priority}` },
          { type: 'mrkdwn', text: `*Status:*\n${ticket.status}` }
        ]
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Description:*\n>${ticket.description.slice(0, 200).replace(/\n/g, '\n>')}${ticket.description.length > 200 ? '...' : ''}`
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Plan:*\n${plan.map(s => `• ${s}`).join('\n')}`
        }
      },
      {
        type: 'actions',
        elements: [
          {
            type: 'button',
            text: { type: 'plain_text', text: '🔗 Open in Freshdesk', emoji: true },
            url: `https://${process.env.FRESHDESK_DOMAIN}/a/tickets/${ticket.id}`
          }
        ]
      }
    ]
  };

  try {
    await axios.post(SLACK_WEBHOOK_URL, message);
    console.log(chalk.green(`  ✓ Posted to Slack`));
  } catch (error) {
    console.error(chalk.red(`  ✗ Slack post failed: ${error.message}`));
  }
}

function spawnClaudeSession(ticket, prompt) {
  console.log(chalk.cyan(`  → Spawning Claude Code session for ticket #${ticket.id}...`));

  try {
    // Write prompt to temp file to avoid shell escaping issues
    const tmpFile = `/tmp/claude-ticket-${ticket.id}.md`;
    require('fs').writeFileSync(tmpFile, prompt);

    // Spawn claude in a new terminal
    const terminal = process.env.TERMINAL || 'kitty';

    if (terminal === 'kitty') {
      spawn('kitty', ['--title', `Ticket #${ticket.id}`, 'claude', '-p', prompt], {
        detached: true,
        stdio: 'ignore'
      }).unref();
    } else if (terminal === 'gnome-terminal') {
      spawn('gnome-terminal', ['--', 'claude', '-p', prompt], {
        detached: true,
        stdio: 'ignore'
      }).unref();
    } else {
      // Fallback: just run claude in background
      spawn('claude', ['--print', '-p', prompt], {
        detached: true,
        stdio: 'ignore'
      }).unref();
    }

    console.log(chalk.green(`  ✓ Claude session spawned`));
  } catch (error) {
    console.error(chalk.red(`  ✗ Failed to spawn Claude: ${error.message}`));
  }
}

main();
