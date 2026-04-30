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

import { writeFileSync, readFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';

function spawnClaudeSession(event, prompt, userName, channelName) {
  console.log(chalk.cyan(`  → Delivering to Claude Code...`));

  // Always queue for MCP (if configured in current session)
  tryInjectCurrentSession(prompt, userName, channelName);

  // Always spawn terminal for immediate handling
  const spawned = trySpawnTerminal(prompt, userName);
  if (spawned) return;

  // Fallback: Open Claude Code web
  tryOpenWeb(prompt, userName);
}

function tryInjectCurrentSession(prompt, userName, channelName) {
  try {
    const queueFile = process.env.CLAUDE_SESSION_FILE || '/tmp/claude-ticket-queue.json';

    let queue = [];
    if (existsSync(queueFile)) {
      try { queue = JSON.parse(readFileSync(queueFile, 'utf8')); } catch {}
    }

    queue.push({
      type: 'slack',
      from: userName,
      channel: channelName,
      prompt,
      queuedAt: new Date().toISOString()
    });

    writeFileSync(queueFile, JSON.stringify(queue, null, 2));

    // Send desktop notification
    try {
      execSync(`notify-send -u critical "Support Request" "From ${userName} in #${channelName}" 2>/dev/null`);
    } catch {}

    console.log(chalk.green(`  ✓ Queued for current session + notified`));
    return true;
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Could not queue: ${e.message}`));
    return false;
  }
}

function trySpawnTerminal(prompt, userName) {
  const terminals = ['kitty', 'alacritty', 'wezterm', 'gnome-terminal', 'konsole', 'xterm'];

  for (const term of terminals) {
    try {
      let args;
      switch (term) {
        case 'kitty':
          args = ['--title', `Slack: ${userName}`, 'claude', '-p', prompt];
          break;
        case 'alacritty':
          args = ['--title', `Slack: ${userName}`, '-e', 'claude', '-p', prompt];
          break;
        case 'wezterm':
          args = ['start', '--', 'claude', '-p', prompt];
          break;
        case 'gnome-terminal':
          args = ['--title', `Slack: ${userName}`, '--', 'claude', '-p', prompt];
          break;
        case 'konsole':
          args = ['-e', 'claude', '-p', prompt];
          break;
        case 'xterm':
          args = ['-title', `Slack: ${userName}`, '-e', 'claude', '-p', prompt];
          break;
      }

      spawn(term, args, { detached: true, stdio: 'ignore' }).unref();
      console.log(chalk.green(`  ✓ New terminal spawned (${term})`));
      return true;
    } catch {}
  }

  return false;
}

function tryOpenWeb(prompt, userName) {
  try {
    // Write prompt to temp file for reference
    const tmpFile = `/tmp/claude-slack-${Date.now()}.md`;
    writeFileSync(tmpFile, prompt);

    // Open Claude Code web
    const browsers = ['xdg-open', 'firefox', 'chromium', 'google-chrome'];
    for (const browser of browsers) {
      try {
        spawn(browser, ['https://claude.ai/code'], { detached: true, stdio: 'ignore' }).unref();
        console.log(chalk.green(`  ✓ Opened Claude Code web`));
        console.log(chalk.gray(`    Prompt saved to: ${tmpFile}`));
        return true;
      } catch {}
    }
  } catch (e) {
    console.error(chalk.red(`  ✗ All methods failed: ${e.message}`));
  }
  return false;
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
