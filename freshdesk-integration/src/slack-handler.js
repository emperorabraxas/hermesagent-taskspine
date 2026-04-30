#!/usr/bin/env node
import 'dotenv/config';
import { WebClient } from '@slack/web-api';
import { SocketModeClient } from '@slack/socket-mode';
import { spawn, execSync } from 'child_process';
import { writeFileSync } from 'fs';
import axios from 'axios';
import chalk from 'chalk';

const SLACK_APP_TOKEN = process.env.SLACK_APP_TOKEN;
const SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN;
const JIRA_BASE_URL = process.env.JIRA_BASE_URL;
const JIRA_EMAIL = process.env.JIRA_EMAIL;
const JIRA_API_TOKEN = process.env.JIRA_API_TOKEN;
const JIRA_PROJECT_KEY = process.env.JIRA_PROJECT_KEY || 'UMDT';

if (!SLACK_APP_TOKEN || !SLACK_BOT_TOKEN) {
  console.error(chalk.red('Missing SLACK_APP_TOKEN or SLACK_BOT_TOKEN in .env'));
  process.exit(1);
}

if (!JIRA_BASE_URL || !JIRA_EMAIL || !JIRA_API_TOKEN) {
  console.error(chalk.red('Missing JIRA_BASE_URL, JIRA_EMAIL, or JIRA_API_TOKEN in .env'));
  process.exit(1);
}

const webClient = new WebClient(SLACK_BOT_TOKEN);
const socketClient = new SocketModeClient({ appToken: SLACK_APP_TOKEN });

const seenMessages = new Set();
const pendingApprovals = new Map();

// Code issues → Robert (terminal), non-code → Jira ticket
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

const MILAD_HANDLE = 'Milad Romaya';
let MILAD_ID = 'U06HUEDMPU1';

const SUPPORT_KEYWORDS = [
  'help', 'error', 'issue', 'broken', 'not working', 'bug', 'problem',
  'cant', "can't", 'cannot', 'failed', 'failing', 'stuck', 'crash',
  'how do i', 'how to', 'please', 'urgent', 'asap', 'need'
];

console.log(chalk.cyan('╔════════════════════════════════════════════╗'));
console.log(chalk.cyan('║') + chalk.white.bold('  TicketsPlease                             ') + chalk.cyan('║'));
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
  await handleMessage(event, true);
});

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
  const isSupport = isMention || SUPPORT_KEYWORDS.some(kw => text.includes(kw));
  if (!isSupport) return;

  let userName = 'there';
  try {
    const user = await webClient.users.info({ user: event.user });
    userName = user.user?.real_name?.split(' ')[0] || user.user?.name || 'there';
  } catch {}

  console.log(chalk.yellow(`\n🎫 Support request from ${userName}`));
  console.log(chalk.gray(`   "${event.text?.slice(0, 80)}${event.text?.length > 80 ? '...' : ''}"`));

  const analysis = await analyzeWithClaude(event.text || '', userName);

  if (analysis.needsTerminal) {
    console.log(chalk.cyan(`  → Escalating, sending to Milad for approval...`));
    await replyToSlack(event, `Hey ${userName}! I'm escalating this to the team — someone will follow up shortly.`);
    const isCodeIssue = detectCodeIssue(event.text || '');
    await dmMiladForApproval(event, userName, analysis.questions || 'Needs investigation', isCodeIssue);
  } else {
    console.log(chalk.cyan(`  → Auto-replying...`));
    await replyToSlack(event, analysis.response);
  }
}

async function analyzeWithClaude(message, userName) {
  const prompt = `${SYSTEM_CONTEXT}

Analyze this support message and decide how to handle it.

Message from ${userName}: "${message}"

Rules (follow exactly):
1. If this requires code changes (Salesforce, AWS, UWM integration code) → needsTerminal: true
2. Only set needsTerminal: false if you can answer COMPLETELY and DEFINITIVELY with zero missing context.
3. If there is ANY uncertainty, vagueness, or missing info → needsTerminal: true.
4. NEVER put a question in the "response" field. The response field is for complete final answers only.
5. If you have questions, put them in the "questions" field and set needsTerminal: true.
6. When in doubt, escalate. Do not ask the submitter for clarification.

Respond in this exact JSON format only, no other text:

If you can FULLY answer without needing anything else:
{"needsTerminal": false, "response": "Your complete answer here"}

If there is ANY uncertainty or missing info:
{"needsTerminal": true, "questions": "What specifically needs investigation"}`;

  try {
    const tmpFile = `/tmp/claude-analyze-${Date.now()}.txt`;
    writeFileSync(tmpFile, prompt);

    const result = execSync(`claude --print -p "$(cat ${tmpFile})" 2>/dev/null`, {
      encoding: 'utf8',
      timeout: 30000
    }).trim();

    const jsonMatch = result.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      if (!parsed.needsTerminal && parsed.response?.includes('?')) {
        return { needsTerminal: true, questions: parsed.response };
      }
      return {
        needsTerminal: parsed.needsTerminal || false,
        response: parsed.response || `Hey ${userName}! I'm escalating this to the team — someone will follow up shortly.`,
        questions: parsed.questions
      };
    }
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Claude analysis failed: ${e.message}`));
  }

  return {
    needsTerminal: true,
    questions: 'Could not analyze — needs human review'
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

async function createJiraTicket(ticket) {
  const auth = Buffer.from(`${JIRA_EMAIL}:${JIRA_API_TOKEN}`).toString('base64');
  const summary = `Support: ${ticket.userName} — ${(ticket.event.text || '').slice(0, 80)}`;

  const response = await axios.post(
    `${JIRA_BASE_URL}/rest/api/3/issue`,
    {
      fields: {
        project: { key: JIRA_PROJECT_KEY },
        summary,
        description: {
          type: 'doc',
          version: 1,
          content: [
            {
              type: 'paragraph',
              content: [{ type: 'text', text: `From: ${ticket.userName}` }]
            },
            {
              type: 'paragraph',
              content: [{ type: 'text', text: `Message: ${ticket.event.text || ''}` }]
            },
            {
              type: 'paragraph',
              content: [{ type: 'text', text: `Notes: ${ticket.reason || ''}` }]
            }
          ]
        },
        issuetype: { name: 'Task' }
      }
    },
    {
      headers: {
        Authorization: `Basic ${auth}`,
        'Content-Type': 'application/json',
        Accept: 'application/json'
      }
    }
  );

  return response.data;
}

socketClient.on('reaction_added', async ({ event, ack }) => {
  await ack();

  const ticket = pendingApprovals.get(event.item.ts);
  if (!ticket) return;

  if (event.reaction === '+1' || event.reaction === 'thumbsup') {
    console.log(chalk.green(`  ✓ Approved by Milad`));
    pendingApprovals.delete(event.item.ts);

    if (ticket.isCodeIssue) {
      console.log(chalk.cyan(`  → Code issue → spawning terminal for Robert`));
      spawnTerminal(ticket.event, ticket.userName, ticket.reason);
      try { execSync(`notify-send -u critical "Support approved" "${ticket.event.text?.slice(0, 50)}..."`); } catch {}
    } else {
      console.log(chalk.cyan(`  → Non-code issue → creating Jira ticket`));
      try {
        const jira = await createJiraTicket(ticket);
        const issueUrl = `${JIRA_BASE_URL}/browse/${jira.key}`;
        console.log(chalk.green(`  ✓ Jira ticket created: ${jira.key}`));
        await replyToSlack(ticket.event, `Your request has been logged — ticket ${jira.key} created. The team will follow up shortly.`);
      } catch (e) {
        console.log(chalk.red(`  ✗ Jira create failed: ${e.message}`));
      }
    }
  } else if (event.reaction === '-1' || event.reaction === 'thumbsdown') {
    console.log(chalk.yellow(`  → Rejected by Milad`));
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
    }
  } catch (e) {
    console.log(chalk.yellow(`Could not lookup users: ${e.message}`));
  }
}

async function dmMiladForApproval(event, userName, reason, isCodeIssue) {
  const routeTo = isCodeIssue ? 'Robert (terminal)' : 'Jira (UMDT)';

  try {
    const result = await webClient.chat.postMessage({
      channel: MILAD_ID,
      text: `🎫 *New Support Request*\n\n*From:* ${userName}\n*Message:* ${event.text}\n*Reason:* ${reason}\n*Route to:* ${routeTo}\n\nReact 👍 to approve, 👎 to reject.`
    });

    pendingApprovals.set(result.ts, { event, userName, reason, isCodeIssue });
    console.log(chalk.green(`  ✓ Sent to Milad for approval`));
  } catch (e) {
    console.log(chalk.yellow(`  ⚠ Could not DM Milad: ${e.message}`));
    if (isCodeIssue) spawnTerminal(event, userName, reason);
  }
}

function spawnTerminal(event, userName, reason = '') {
  const prompt = `Escalated support request from ${userName}: ${event.text || 'No message'}\n\nReason: ${reason || 'Unknown'}\n\nInvestigate and fix this issue.`;
  const promptFile = `/tmp/claude-support-${Date.now()}.txt`;
  writeFileSync(promptFile, prompt);

  const sessionName = `support-${Date.now()}`;
  try {
    execSync(`tmux new-session -d -s ${sessionName} -c ~/hermesagent-taskspine 'claude'`);
    setTimeout(() => {
      try {
        execSync(`tmux send-keys -t ${sessionName} -l ${JSON.stringify(prompt)}`);
        execSync(`tmux send-keys -t ${sessionName} Enter`);
        console.log(chalk.green(`  ✓ Prompt sent to Claude`));
      } catch (e) {
        console.log(chalk.yellow(`  ⚠ Could not send text: ${e.message}`));
      }
    }, 3000);

    spawn('kitty', ['--title', `Support: ${userName}`, 'tmux', 'attach', '-t', sessionName], {
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
    await lookupUsers();
    console.log(chalk.gray('Listening for support requests...\n'));
  } catch (error) {
    console.error(chalk.red('Failed to connect:'), error.message);
    process.exit(1);
  }
})();
