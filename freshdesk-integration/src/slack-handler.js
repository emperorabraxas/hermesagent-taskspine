#!/usr/bin/env node
import 'dotenv/config';
import { WebClient } from '@slack/web-api';
import { SocketModeClient } from '@slack/socket-mode';
import { spawn } from 'child_process';
import chalk from 'chalk';

const SLACK_APP_TOKEN = process.env.SLACK_APP_TOKEN;
const SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN;

if (!SLACK_APP_TOKEN || !SLACK_BOT_TOKEN) {
  console.error(chalk.red('Missing SLACK_APP_TOKEN or SLACK_BOT_TOKEN in .env'));
  process.exit(1);
}

const webClient = new WebClient(SLACK_BOT_TOKEN);
const socketClient = new SocketModeClient({ appToken: SLACK_APP_TOKEN });

const seenMessages = new Set();

console.log(chalk.cyan('╔════════════════════════════════════════════╗'));
console.log(chalk.cyan('║') + chalk.white.bold('  Slack → Claude Code Integration           ') + chalk.cyan('║'));
console.log(chalk.cyan('╚════════════════════════════════════════════╝'));

socketClient.on('message', async ({ event, ack }) => {
  await ack();

  // Skip bot messages, message edits, and already-seen messages
  if (event.bot_id || event.subtype || seenMessages.has(event.ts)) return;
  seenMessages.add(event.ts);

  // Get channel info
  let channelName = event.channel;
  try {
    const info = await webClient.conversations.info({ channel: event.channel });
    channelName = info.channel?.name || event.channel;
  } catch {}

  // Get user info
  let userName = 'Unknown';
  try {
    const user = await webClient.users.info({ user: event.user });
    userName = user.user?.real_name || user.user?.name || 'Unknown';
  } catch {}

  console.log(chalk.yellow(`\n🎫 Support request from ${userName} in #${channelName}`));
  console.log(chalk.gray(`   "${event.text?.slice(0, 100)}${event.text?.length > 100 ? '...' : ''}"`));

  const prompt = generatePrompt(event, userName, channelName);
  spawnClaudeSession(event, prompt, userName, channelName);
});

socketClient.on('app_mention', async ({ event, ack }) => {
  await ack();

  if (seenMessages.has(event.ts)) return;
  seenMessages.add(event.ts);

  let userName = 'Unknown';
  try {
    const user = await webClient.users.info({ user: event.user });
    userName = user.user?.real_name || user.user?.name || 'Unknown';
  } catch {}

  let channelName = event.channel;
  try {
    const info = await webClient.conversations.info({ channel: event.channel });
    channelName = info.channel?.name || event.channel;
  } catch {}

  console.log(chalk.yellow(`\n🔔 Mentioned by ${userName} in #${channelName}`));
  console.log(chalk.gray(`   "${event.text?.slice(0, 100)}${event.text?.length > 100 ? '...' : ''}"`));

  const prompt = generatePrompt(event, userName, channelName);
  spawnClaudeSession(event, prompt, userName, channelName);
});

function generatePrompt(event, userName, channelName) {
  const plan = generatePlan(event.text || '');

  return `## Slack Support Request

**From:** ${userName}
**Channel:** #${channelName}
**Time:** ${new Date(parseFloat(event.ts) * 1000).toLocaleString()}

### Message
${event.text || '(no text)'}

### Suggested Plan
${plan.map((s, i) => `${i + 1}. ${s}`).join('\n')}

---

Help me handle this support request:
1. Understand what they need
2. Draft a response
3. If code changes needed, identify them`;
}

function generatePlan(text) {
  const lower = text.toLowerCase();

  if (lower.includes('error') || lower.includes('bug') || lower.includes('broken') || lower.includes('not working')) {
    return ['Identify the error', 'Check for known issues', 'Draft fix or workaround'];
  } else if (lower.includes('how') || lower.includes('help') || lower.includes('?')) {
    return ['Understand the question', 'Research answer', 'Draft helpful response'];
  } else if (lower.includes('feature') || lower.includes('request') || lower.includes('add')) {
    return ['Document the request', 'Assess feasibility', 'Draft response'];
  }
  return ['Analyze request', 'Determine action needed', 'Draft response'];
}

function spawnClaudeSession(event, prompt, userName, channelName) {
  console.log(chalk.cyan(`  → Spawning Claude Code session...`));

  try {
    const terminals = ['kitty', 'alacritty', 'wezterm', 'gnome-terminal', 'xterm'];
    let spawned = false;

    for (const term of terminals) {
      try {
        if (term === 'kitty') {
          spawn('kitty', ['--title', `Slack: ${userName}`, 'claude', '-p', prompt], {
            detached: true,
            stdio: 'ignore'
          }).unref();
          spawned = true;
        } else if (term === 'gnome-terminal') {
          spawn('gnome-terminal', ['--title', `Slack: ${userName}`, '--', 'claude', '-p', prompt], {
            detached: true,
            stdio: 'ignore'
          }).unref();
          spawned = true;
        } else if (term === 'alacritty') {
          spawn('alacritty', ['--title', `Slack: ${userName}`, '-e', 'claude', '-p', prompt], {
            detached: true,
            stdio: 'ignore'
          }).unref();
          spawned = true;
        } else if (term === 'wezterm') {
          spawn('wezterm', ['start', '--', 'claude', '-p', prompt], {
            detached: true,
            stdio: 'ignore'
          }).unref();
          spawned = true;
        }
        if (spawned) {
          console.log(chalk.green(`  ✓ Claude session spawned (${term})`));
          break;
        }
      } catch {}
    }

    if (!spawned) {
      // Fallback: run claude directly
      spawn('claude', ['-p', prompt], {
        detached: true,
        stdio: 'ignore'
      }).unref();
      console.log(chalk.green(`  ✓ Claude session spawned`));
    }
  } catch (error) {
    console.error(chalk.red(`  ✗ Failed to spawn: ${error.message}`));
  }
}

(async () => {
  try {
    await socketClient.start();
    console.log(chalk.green('✓ Connected to Slack'));
    console.log(chalk.gray('Listening for messages...\n'));
  } catch (error) {
    console.error(chalk.red('Failed to connect:'), error.message);
    process.exit(1);
  }
})();
