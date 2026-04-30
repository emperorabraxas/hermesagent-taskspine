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

// System context for Claude
const SYSTEM_CONTEXT = `You are a support bot for a Salesforce-AWS-UWM integration system.

Stack context:
- Salesforce LWC components (Lightning Web Components)
- AWS Lambda functions
- UWM (United Wholesale Mortgage) API integration
- Auth token handling and refresh flows
- Loan processing workflows

Your job is to analyze support messages and respond appropriately.`;

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

  // Use Claude to analyze and respond
  const analysis = await analyzeWithClaude(event.text || '', userName);

  if (analysis.needsTerminal) {
    console.log(chalk.cyan(`  → Code issue detected, spawning terminal...`));
    await replyToSlack(event, `Hey ${userName}! Looking into this now — I'll get back to you shortly.`);
    spawnTerminal(event, userName);
  } else {
    console.log(chalk.cyan(`  → Auto-replying...`));
    await replyToSlack(event, analysis.response);
  }
}

async function analyzeWithClaude(message, userName) {
  const prompt = `${SYSTEM_CONTEXT}

Analyze this support message and respond.

Message from ${userName}: "${message}"

Instructions:
1. Determine if this requires code changes (Salesforce, AWS, UWM integration code) → set needsTerminal: true
2. If it's a general question, login issue, or can be answered directly → provide a helpful response
3. Keep responses concise and friendly

Respond in this exact JSON format only, no other text:
{"needsTerminal": true/false, "response": "your response here"}`;

  try {
    const tmpFile = `/tmp/claude-analyze-${Date.now()}.txt`;
    writeFileSync(tmpFile, prompt);

    const result = execSync(`claude --print -p "$(cat ${tmpFile})" 2>/dev/null`, {
      encoding: 'utf8',
      timeout: 30000
    }).trim();

    // Parse JSON from response
    const jsonMatch = result.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      return {
        needsTerminal: parsed.needsTerminal || false,
        response: parsed.response || `Hey ${userName}! Got your message, looking into it.`
      };
    }
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Claude analysis failed: ${e.message}`));
  }

  // Fallback
  return {
    needsTerminal: false,
    response: `Hey ${userName}! Got your message. Can you give me a bit more detail?`
  };
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
  const prompt = `## Slack Support — Code Issue

**From:** ${userName}
**Message:** ${event.text}

${SYSTEM_CONTEXT}

Analyze this issue and help me fix it. After we solve it, draft a response to send back.`;

  const tmpFile = `/tmp/claude-prompt-${Date.now()}.md`;
  writeFileSync(tmpFile, prompt);

  // Interactive session (no --print) so it stays open
  const claudeCmd = `claude -p "$(cat ${tmpFile})"`;

  try {
    spawn('kitty', ['--title', `Support: ${userName}`, 'bash', '-c', claudeCmd], {
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
