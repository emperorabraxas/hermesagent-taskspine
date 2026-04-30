#!/usr/bin/env node
import 'dotenv/config';
import { FreshdeskClient } from './freshdesk-client.js';
import { ClaudeNotifier } from './claude-notifier.js';
import chalk from 'chalk';
import ora from 'ora';

const POLL_INTERVAL = parseInt(process.env.POLL_INTERVAL_MS || '30000', 10);
const seenTickets = new Map();

async function main() {
  const domain = process.env.FRESHDESK_DOMAIN;
  const apiKey = process.env.FRESHDESK_API_KEY;

  if (!domain || !apiKey) {
    console.error(chalk.red('Missing FRESHDESK_DOMAIN or FRESHDESK_API_KEY in .env'));
    process.exit(1);
  }

  const client = new FreshdeskClient(domain, apiKey);
  const notifier = new ClaudeNotifier();

  console.log(chalk.cyan('╔════════════════════════════════════════════╗'));
  console.log(chalk.cyan('║') + chalk.white.bold('  Freshdesk → Claude Code Integration      ') + chalk.cyan('║'));
  console.log(chalk.cyan('╚════════════════════════════════════════════╝'));
  console.log(chalk.gray(`Polling ${domain} every ${POLL_INTERVAL / 1000}s...\n`));

  async function poll() {
    const spinner = ora({ text: 'Checking for new tickets...', color: 'cyan' }).start();

    try {
      const tickets = await client.getNewOrUpdatedTickets(5);
      spinner.stop();

      for (const ticket of tickets) {
        const lastSeen = seenTickets.get(ticket.id);
        const ticketUpdated = new Date(ticket.updated_at).getTime();

        if (!lastSeen || ticketUpdated > lastSeen) {
          seenTickets.set(ticket.id, ticketUpdated);

          const fullTicket = await client.getTicket(ticket.id);
          const formatted = client.formatTicketForClaude(fullTicket);

          console.log(chalk.yellow(`\n🎫 ${lastSeen ? 'Updated' : 'New'} Ticket #${ticket.id}`));
          console.log(chalk.white(`   Subject: ${formatted.subject}`));
          console.log(chalk.gray(`   Priority: ${formatted.priority} | Status: ${formatted.status}`));

          await notifier.queueTicket(formatted, lastSeen ? 'updated' : 'new');
        }
      }

      if (tickets.length === 0) {
        console.log(chalk.gray(`[${new Date().toLocaleTimeString()}] No new activity`));
      }
    } catch (error) {
      spinner.stop();
      if (error.response?.status === 401) {
        console.error(chalk.red('Authentication failed. Check your API key.'));
        process.exit(1);
      }
      console.error(chalk.red(`Poll error: ${error.message}`));
    }
  }

  await poll();
  setInterval(poll, POLL_INTERVAL);

  process.on('SIGINT', () => {
    console.log(chalk.cyan('\nShutting down poller...'));
    process.exit(0);
  });
}

main();
