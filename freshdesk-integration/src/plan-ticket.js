#!/usr/bin/env node
import 'dotenv/config';
import { FreshdeskClient } from './freshdesk-client.js';
import { ClaudeNotifier } from './claude-notifier.js';
import chalk from 'chalk';
import { execSync, spawn } from 'child_process';

async function main() {
  const ticketId = process.argv[2];
  const mode = process.argv[3] || 'plan';

  if (!ticketId) {
    console.log(chalk.cyan('Usage: npm run plan -- <ticket_id> [mode]'));
    console.log(chalk.gray('  Modes: plan (default), execute, print'));
    console.log('');

    const notifier = new ClaudeNotifier();
    const unprocessed = notifier.getUnprocessedTickets();

    if (unprocessed.length > 0) {
      console.log(chalk.yellow(`Unprocessed tickets in queue:`));
      for (const entry of unprocessed) {
        console.log(chalk.white(`  #${entry.ticket.id}: ${entry.ticket.subject}`));
      }
    } else {
      console.log(chalk.gray('No tickets in queue. Run the poller first: npm run poll'));
    }
    return;
  }

  const domain = process.env.FRESHDESK_DOMAIN;
  const apiKey = process.env.FRESHDESK_API_KEY;

  if (!domain || !apiKey) {
    console.error(chalk.red('Missing FRESHDESK_DOMAIN or FRESHDESK_API_KEY in .env'));
    process.exit(1);
  }

  const client = new FreshdeskClient(domain, apiKey);
  const notifier = new ClaudeNotifier();

  console.log(chalk.cyan(`Fetching ticket #${ticketId}...`));

  try {
    const ticket = await client.getTicket(ticketId);
    const formatted = client.formatTicketForClaude(ticket);

    const prompt = generateClaudePrompt(formatted);

    if (mode === 'print') {
      console.log('\n' + chalk.green('─── Claude Prompt ───'));
      console.log(prompt);
    } else if (mode === 'execute') {
      console.log(chalk.cyan('\nLaunching Claude Code with ticket context...\n'));
      launchClaudeCode(prompt);
      notifier.markProcessed(ticketId);
    } else {
      console.log('\n' + chalk.green('─── Generated Plan ───'));
      console.log(prompt);
      console.log(chalk.cyan('\n💡 To execute this in Claude Code:'));
      console.log(chalk.white(`   npm run plan -- ${ticketId} execute`));
      console.log(chalk.gray('   Or copy the prompt above into your Claude Code session.\n'));
    }
  } catch (error) {
    if (error.response?.status === 404) {
      console.error(chalk.red(`Ticket #${ticketId} not found`));
    } else {
      console.error(chalk.red(`Error: ${error.message}`));
    }
    process.exit(1);
  }
}

function generateClaudePrompt(ticket) {
  const conversationContext = ticket.conversations.length > 0
    ? ticket.conversations.map(c =>
        `[${c.incoming ? 'Customer' : 'Support'}] ${c.body.slice(0, 500)}`
      ).join('\n\n')
    : 'No previous replies.';

  return `## Support Ticket #${ticket.id}

**Subject:** ${ticket.subject}
**From:** ${ticket.requester} <${ticket.requesterEmail || 'unknown'}>
**Priority:** ${ticket.priority} | **Status:** ${ticket.status}
**Tags:** ${ticket.tags.length > 0 ? ticket.tags.join(', ') : 'none'}

### Description
${ticket.description}

### Conversation History
${conversationContext}

---

### Task
Analyze this support ticket and help me:
1. Understand the core issue/request
2. Identify what information or action is needed
3. Draft a helpful response

If this requires code changes, identify the files and changes needed.
If this is a question, research the answer.
If this needs escalation, explain why.`;
}

function launchClaudeCode(prompt) {
  const escapedPrompt = prompt.replace(/'/g, "'\\''");

  try {
    const claude = spawn('claude', ['--print', '-p', prompt], {
      stdio: 'inherit',
      shell: true
    });

    claude.on('error', (err) => {
      console.error(chalk.red(`Failed to launch claude: ${err.message}`));
      console.log(chalk.yellow('Make sure Claude Code CLI is installed and in your PATH.'));
      console.log(chalk.gray('Falling back to clipboard copy...\n'));
      copyToClipboard(prompt);
    });
  } catch (error) {
    console.log(chalk.yellow('Claude CLI not available. Copying prompt to clipboard...'));
    copyToClipboard(prompt);
  }
}

function copyToClipboard(text) {
  try {
    if (process.platform === 'darwin') {
      execSync('pbcopy', { input: text });
      console.log(chalk.green('✓ Prompt copied to clipboard. Paste into Claude Code.'));
    } else if (process.platform === 'linux') {
      execSync('xclip -selection clipboard', { input: text });
      console.log(chalk.green('✓ Prompt copied to clipboard. Paste into Claude Code.'));
    } else {
      console.log(chalk.yellow('Could not copy to clipboard. Copy the prompt above manually.'));
    }
  } catch {
    console.log(chalk.yellow('Clipboard not available. Copy the prompt above manually.'));
  }
}

main();
