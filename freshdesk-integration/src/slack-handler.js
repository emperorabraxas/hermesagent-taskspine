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
const pendingApprovals = new Map(); // messageTs -> ticket data

// Detect if issue is code-related (goes to Robert) or general (goes to Joe)
function detectCodeIssue(text) {
  const lower = text.toLowerCase();
  const codeKeywords = [
    'code', 'bug', 'error', 'api', 'deploy', 'server', 'database', 'function',
    'lambda', 'salesforce', 'apex', 'lwc', 'uwm', 'integration', 'import',
    'export', 'sync', 'auth', 'token', 'login', 'crash', 'exception',
    'build', 'git', 'commit', 'merge', 'test', 'ci', 'pipeline', 'aws'
  ];
  return codeKeywords.some(kw => lower.includes(kw));
}

// Team routing
const MILAD_HANDLE = 'Milad Romaya';
const JOE_HANDLE = 'Joseph DeMasse';
let MILAD_ID = 'U06HUEDMPU1';
let JOE_ID = 'U093L2520MP';

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
    console.log(chalk.cyan(`  → Needs investigation, sending to Milad for approval...`));
    await replyToSlack(event, `Hey ${userName}! I'm escalating this to the team — someone will follow up shortly.`);

    // Determine if code issue or general issue
    const isCodeIssue = detectCodeIssue(event.text || '');
    await dmMiladForApproval(event, userName, analysis.questions || 'Needs investigation', isCodeIssue);
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

If you can FULLY answer/solve without needing any more information:
{"needsTerminal": false, "response": "Your complete solution/answer"}

If you need ANY additional info, clarification, or aren't 100% sure:
{"needsTerminal": true, "response": "I'm escalating this to the team.", "questions": "What you need to investigate"}`;

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

function tryAutoSolve(event, userName) {
  const responseFile = `/tmp/claude-response-${Date.now()}.json`;

  const prompt = `${SYSTEM_CONTEXT}

## Support Request
**From:** ${userName}
**Message:** ${event.text}

## Instructions
1. Investigate this issue - check the codebase, look for relevant files, understand the problem
2. Try to fix it if you can identify the issue
3. When done, respond with ONLY this JSON (no other text):

If you solved it completely:
{"solved": true, "response": "Your solution to send to Slack"}

If you need ANY additional info, have questions, or need human help:
{"solved": false, "questions": "What you need to know to solve this"}`;

  const tmpFile = `/tmp/claude-prompt-${Date.now()}.md`;
  writeFileSync(tmpFile, prompt);

  console.log(chalk.cyan(`  → Claude investigating in background...`));

  // Run in background
  const claude = spawn('bash', ['-c', `cd ~/hermesagent-taskspine && claude --print -p "$(cat ${tmpFile})"`], {
    stdio: ['ignore', 'pipe', 'pipe']
  });

  let output = '';
  claude.stdout.on('data', (data) => { output += data.toString(); });
  claude.stderr.on('data', (data) => { output += data.toString(); });

  claude.on('close', async (code) => {
    console.log(chalk.cyan(`  → Claude finished (exit ${code})`));

    try {
      const jsonMatch = output.match(/\{[\s\S]*"solved"[\s\S]*\}/);

      if (jsonMatch) {
        const result = JSON.parse(jsonMatch[0]);

        if (result.solved) {
          console.log(chalk.green(`  ✓ Solved, auto-replying`));
          await replyToSlack(event, result.response);
        } else {
          // Not solved - escalate to human, don't ask submitter
          console.log(chalk.yellow(`  → Escalating to human`));
          await replyToSlack(event, `Hey ${userName}! I'm escalating this to the team — someone will follow up shortly.`);
          spawnTerminal(event, userName, result.questions || 'Needs investigation');
          try { execSync(`notify-send -u critical "Support escalated" "${event.text?.slice(0, 50)}..."`); } catch {}
        }
        return;
      }
    } catch (e) {
      console.log(chalk.yellow(`  ⚠ Parse failed: ${e.message}`));
    }

    // Fallback - escalate
    console.log(chalk.yellow(`  → Escalating (couldn't parse)`));
    await replyToSlack(event, `Hey ${userName}! I'm escalating this to the team — someone will follow up shortly.`);
    spawnTerminal(event, userName, 'Auto-solve unclear');
    try { execSync(`notify-send -u critical "Support escalated" "${event.text?.slice(0, 50)}..."`); } catch {}
  });
}

function spawnTerminal(event, userName, reason = '') {
  const promptFile = `/tmp/claude-support-${Date.now()}.txt`;
  const prompt = `Escalated support request from ${userName}: ${event.text || 'No message'}\n\nReason escalated: ${reason || 'Unknown'}\n\nInvestigate and fix this issue.`;

  writeFileSync(promptFile, prompt);

  // Use tmux to send text reliably
  const sessionName = `support-${Date.now()}`;

  try {
    // Create tmux session running claude
    execSync(`tmux new-session -d -s ${sessionName} -c ~/hermesagent-taskspine 'claude'`);

    // Wait for claude to start
    setTimeout(() => {
      try {
        // Send the prompt text
        execSync(`tmux send-keys -t ${sessionName} -l ${JSON.stringify(prompt)}`);
        execSync(`tmux send-keys -t ${sessionName} Enter`);
        console.log(chalk.green(`  ✓ Prompt sent to Claude`));
      } catch (e) {
        console.log(chalk.yellow(`  ⚠ Could not send text: ${e.message}`));
      }
    }, 3000);

    // Open kitty attached to the tmux session
    spawn('kitty', ['--title', `Support: ${userName}`, 'tmux', 'attach', '-t', sessionName], {
      detached: true,
      stdio: 'ignore'
    }).unref();

    console.log(chalk.green(`  ✓ Terminal spawned`));
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Terminal failed: ${e.message}`));
  }
}

// Handle reaction approvals
socketClient.on('reaction_added', async ({ event, ack }) => {
  await ack();

  // Check if this is an approval reaction on a pending ticket
  const ticket = pendingApprovals.get(event.item.ts);
  if (!ticket) return;

  if (event.reaction === '+1' || event.reaction === 'thumbsup') {
    console.log(chalk.green(`  ✓ Ticket approved by Milad`));
    pendingApprovals.delete(event.item.ts);

    // Route based on ticket type
    if (ticket.isCodeIssue) {
      console.log(chalk.cyan(`  → Routing to terminal (code issue)`));
      spawnTerminal(ticket.event, ticket.userName, ticket.reason);
      try { execSync(`notify-send -u critical "Support approved" "${ticket.event.text?.slice(0, 50)}..."`); } catch {}
    } else {
      console.log(chalk.cyan(`  → Routing to Joe (non-code issue)`));
      await dmJoe(ticket);
    }
  } else if (event.reaction === '-1' || event.reaction === 'thumbsdown') {
    console.log(chalk.yellow(`  → Ticket rejected by Milad`));
    pendingApprovals.delete(event.item.ts);
    await replyToSlack(ticket.event, `Update: We've reviewed your request and will follow up if needed.`);
  }
});

async function lookupUsers() {
  try {
    const result = await webClient.users.list();
    for (const user of result.members) {
      if (user.real_name === MILAD_HANDLE || user.profile?.real_name === MILAD_HANDLE) {
        MILAD_ID = user.id;
        console.log(chalk.gray(`Found Milad: ${MILAD_ID}`));
      }
      if (user.real_name === JOE_HANDLE || user.profile?.real_name === JOE_HANDLE) {
        JOE_ID = user.id;
        console.log(chalk.gray(`Found Joe: ${JOE_ID}`));
      }
    }
  } catch (e) {
    console.log(chalk.yellow(`Could not lookup users: ${e.message}`));
  }
}

async function dmMiladForApproval(event, userName, reason, isCodeIssue) {
  if (!MILAD_ID) {
    console.log(chalk.yellow(`  ⚠ Milad ID not found, routing directly`));
    if (isCodeIssue) {
      spawnTerminal(event, userName, reason);
    } else {
      await dmJoe({ event, userName, reason });
    }
    return;
  }

  try {
    const routeTo = isCodeIssue ? 'Robert (terminal)' : 'Joe (DM)';
    const result = await webClient.chat.postMessage({
      channel: MILAD_ID,
      text: `🎫 *New Support Request*\n\n*From:* ${userName}\n*Message:* ${event.text}\n*Reason:* ${reason}\n*Route to:* ${routeTo}\n\nReact 👍 to approve, 👎 to reject.`
    });

    // Store for reaction handling
    pendingApprovals.set(result.ts, { event, userName, reason, isCodeIssue });
    console.log(chalk.green(`  ✓ Sent to Milad for approval`));
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Could not DM Milad: ${e.message}`));
    // Fallback - route directly
    if (isCodeIssue) {
      spawnTerminal(event, userName, reason);
    }
  }
}

async function dmJoe(ticket) {
  if (!JOE_ID) {
    console.log(chalk.yellow(`  ⚠ Joe ID not found`));
    return;
  }

  try {
    await webClient.chat.postMessage({
      channel: JOE_ID,
      text: `🎫 *Support Request Assigned to You*\n\n*From:* ${ticket.userName}\n*Message:* ${ticket.event.text}\n*Notes:* ${ticket.reason}\n\nPlease follow up with the customer.`
    });
    console.log(chalk.green(`  ✓ Sent to Joe`));
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Could not DM Joe: ${e.message}`));
  }
}

(async () => {
  try {
    await socketClient.start();
    console.log(chalk.green('✓ Connected to Slack'));
    await lookupUsers();
    console.log(chalk.gray('Listening for support requests...\n'));
  } catch (error) {
    console.error(chalk.red('Failed to connect:'), error.message);
    process.exit(1);
  }
})();
