#!/usr/bin/env node
import 'dotenv/config';
import { WebClient } from '@slack/web-api';
import { SocketModeClient } from '@slack/socket-mode';
import { spawn, execSync } from 'child_process';
import { writeFileSync, readFileSync, existsSync } from 'fs';
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

// Keywords that trigger support response
const SUPPORT_KEYWORDS = [
  'help', 'error', 'issue', 'broken', 'not working', 'bug', 'problem',
  'cant', "can't", 'cannot', 'failed', 'failing', 'stuck', 'crash',
  'how do i', 'how to', 'please', 'urgent', 'asap', 'need'
];

console.log(chalk.cyan('╔════════════════════════════════════════════╗'));
console.log(chalk.cyan('║') + chalk.white.bold('  Slack Auto-Support Bot                    ') + chalk.cyan('║'));
console.log(chalk.cyan('╚════════════════════════════════════════════╝'));
console.log(chalk.gray(`Keywords: ${SUPPORT_KEYWORDS.slice(0, 5).join(', ')}...\n`));

socketClient.on('message', async ({ event, ack }) => {
  await ack();
  if (event.bot_id || event.subtype || seenMessages.has(event.ts)) return;
  seenMessages.add(event.ts);

  await handleMessage(event);
});

socketClient.on('app_mention', async ({ event, ack }) => {
  await ack();
  if (seenMessages.has(event.ts)) return;
  seenMessages.add(event.ts);

  // Always respond to @mentions
  await handleMessage(event, true);
});

async function handleMessage(event, isMention = false) {
  const text = event.text?.toLowerCase() || '';

  // Check if message matches support keywords (or is a mention)
  const isSupport = isMention || SUPPORT_KEYWORDS.some(kw => text.includes(kw));
  if (!isSupport) return;

  // Get user info
  let userName = 'there';
  try {
    const user = await webClient.users.info({ user: event.user });
    userName = user.user?.real_name?.split(' ')[0] || user.user?.name || 'there';
  } catch {}

  console.log(chalk.yellow(`\n🎫 Support request from ${userName}`));
  console.log(chalk.gray(`   "${event.text?.slice(0, 80)}${event.text?.length > 80 ? '...' : ''}"`));

  // Check if it's a code issue that needs terminal
  const codeIssue = needsTerminal(event.text || '');

  if (codeIssue) {
    console.log(chalk.cyan(`  → Code issue, spawning terminal...`));
    await replyToSlack(event, `Hey ${userName}! Looking into this now — I'll get back to you shortly.`);
    spawnTerminal(event, userName);
  } else {
    console.log(chalk.cyan(`  → Generating auto-reply...`));
    const response = await generateResponse(event.text || '', userName);
    await replyToSlack(event, response);
  }
}

function needsTerminal(text) {
  const lower = text.toLowerCase();
  // Only open terminal for issues Claude Code can actually solve
  const codeIssues = [
    'code', 'bug', 'deploy', 'api', 'server', 'database', 'function',
    'script', 'error log', 'stack trace', 'exception', 'crash',
    'build', 'compile', 'git', 'repo', 'branch', 'merge', 'commit',
    'test', 'failing test', 'ci', 'pipeline', 'docker', 'container'
  ];
  return codeIssues.some(kw => lower.includes(kw));
}

async function generateResponse(message, userName) {
  const lower = message.toLowerCase();

  // Login issues
  if (lower.includes('login') || lower.includes('sign in') || lower.includes('password')) {
    return `Hey ${userName}! For login issues, try these quick fixes:

1. **Clear cookies** and try incognito mode
2. **Reset password** via the "Forgot password" link
3. **Check caps lock** — passwords are case-sensitive
4. **Try a different browser**

If still stuck, let me know what error you're seeing and I'll dig deeper.`;
  }

  // Error messages
  if (lower.includes('error') || lower.includes('broken') || lower.includes('not working')) {
    return `Hey ${userName}! Sorry you're hitting an error. To help track this down:

1. What's the **exact error message**?
2. What were you trying to do when it happened?
3. Has this worked before, or is it new?

A screenshot helps a lot if you can grab one!`;
  }

  // How-to questions
  if (lower.includes('how do i') || lower.includes('how to') || lower.includes('?')) {
    return `Hey ${userName}! Happy to help. Can you give me a bit more detail on what you're trying to accomplish? That way I can point you in the right direction.`;
  }

  // Feature requests
  if (lower.includes('feature') || lower.includes('request') || lower.includes('add') || lower.includes('would be nice')) {
    return `Hey ${userName}! Thanks for the suggestion — I've noted it down. Is there a specific workflow this would help with? Context helps prioritize.`;
  }

  // Generic fallback
  return `Hey ${userName}! Got your message. What can I help you with?`;
}

async function replyToSlack(event, text) {
  try {
    await webClient.chat.postMessage({
      channel: event.channel,
      thread_ts: event.ts,
      text
    });
    console.log(chalk.green(`  ✓ Replied in Slack`));
  } catch (e) {
    console.error(chalk.red(`  ✗ Failed to reply: ${e.message}`));
  }
}

function spawnTerminal(event, userName) {
  const prompt = `## Slack Support — Needs Review

**From:** ${userName}
**Message:** ${event.text}

This was flagged as complex. Help me:
1. Understand the issue
2. Determine next steps
3. Draft a response`;

  const tmpFile = `/tmp/claude-prompt-${Date.now()}.md`;
  writeFileSync(tmpFile, prompt);

  const claudeCmd = `claude -p "$(cat ${tmpFile})"`;

  try {
    spawn('kitty', ['--hold', '--title', `Support: ${userName}`, 'bash', '-c', claudeCmd], {
      detached: true,
      stdio: 'ignore'
    }).unref();
    console.log(chalk.green(`  ✓ Terminal spawned`));
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Terminal failed: ${e.message}`));
  }
}

(async () => {
  try {
    await socketClient.start();
    console.log(chalk.green('✓ Connected to Slack'));
    console.log(chalk.gray('Listening for support requests...\n'));
  } catch (error) {
    console.error(chalk.red('Failed to connect:'), error.message);
    process.exit(1);
  }
})();
