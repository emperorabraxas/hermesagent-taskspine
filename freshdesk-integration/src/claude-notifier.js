import { writeFileSync, readFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import chalk from 'chalk';
import boxen from 'boxen';

export class ClaudeNotifier {
  constructor() {
    this.queueFile = process.env.CLAUDE_SESSION_FILE || '/tmp/claude-ticket-queue.json';
    this.notifySound = process.env.NOTIFY_SOUND === 'true';
  }

  async queueTicket(ticket, eventType = 'new') {
    const queue = this.loadQueue();

    const entry = {
      ticket,
      eventType,
      queuedAt: new Date().toISOString(),
      processed: false
    };

    const existingIdx = queue.findIndex(e => e.ticket.id === ticket.id);
    if (existingIdx >= 0) {
      queue[existingIdx] = entry;
    } else {
      queue.push(entry);
    }

    this.saveQueue(queue);
    this.displayNotification(ticket, eventType);

    if (this.notifySound) {
      this.playSound();
    }

    return entry;
  }

  loadQueue() {
    if (!existsSync(this.queueFile)) return [];
    try {
      return JSON.parse(readFileSync(this.queueFile, 'utf8'));
    } catch {
      return [];
    }
  }

  saveQueue(queue) {
    writeFileSync(this.queueFile, JSON.stringify(queue, null, 2));
  }

  displayNotification(ticket, eventType) {
    const plan = this.generatePlan(ticket);

    const content = [
      chalk.bold(`Ticket #${ticket.id}: ${ticket.subject}`),
      '',
      chalk.gray(`From: ${ticket.requester} <${ticket.requesterEmail || 'unknown'}>`),
      chalk.gray(`Priority: ${ticket.priority} | Status: ${ticket.status}`),
      '',
      chalk.cyan('─── Description ───'),
      ticket.description.slice(0, 300) + (ticket.description.length > 300 ? '...' : ''),
      '',
      chalk.green('─── Suggested Plan ───'),
      ...plan.map(step => `  ${step}`)
    ].join('\n');

    console.log(boxen(content, {
      padding: 1,
      margin: 1,
      borderStyle: 'round',
      borderColor: eventType === 'new' ? 'green' : 'yellow',
      title: eventType === 'new' ? '🆕 NEW TICKET' : '🔄 UPDATED TICKET',
      titleAlignment: 'center'
    }));

    console.log(chalk.cyan('\n💡 To handle this ticket in Claude Code, run:'));
    console.log(chalk.white(`   npm run plan -- ${ticket.id}\n`));
  }

  generatePlan(ticket) {
    const steps = [];
    const desc = ticket.description.toLowerCase();
    const subject = ticket.subject.toLowerCase();

    if (desc.includes('error') || desc.includes('bug') || desc.includes('broken') || desc.includes('not working')) {
      steps.push('1. Identify error type and affected component');
      steps.push('2. Check logs/stack traces if provided');
      steps.push('3. Reproduce issue locally if possible');
      steps.push('4. Implement fix and verify');
      steps.push('5. Draft response with resolution details');
    } else if (desc.includes('how to') || desc.includes('help') || subject.includes('question')) {
      steps.push('1. Understand the user\'s goal');
      steps.push('2. Check knowledge base for existing documentation');
      steps.push('3. Draft step-by-step instructions');
      steps.push('4. Include relevant links/resources');
    } else if (desc.includes('feature') || desc.includes('request') || desc.includes('would like')) {
      steps.push('1. Document the feature request');
      steps.push('2. Assess feasibility and scope');
      steps.push('3. Check if similar feature exists');
      steps.push('4. Draft response with timeline/alternatives');
    } else {
      steps.push('1. Analyze ticket content and intent');
      steps.push('2. Gather any missing context');
      steps.push('3. Research solution/answer');
      steps.push('4. Draft response');
    }

    if (ticket.priority === 'Urgent' || ticket.priority === 'High') {
      steps.unshift('⚠️  HIGH PRIORITY - Escalate if blocked');
    }

    return steps;
  }

  playSound() {
    try {
      if (process.platform === 'darwin') {
        execSync('afplay /System/Library/Sounds/Glass.aiff', { stdio: 'ignore' });
      } else if (process.platform === 'linux') {
        execSync('paplay /usr/share/sounds/freedesktop/stereo/message.oga 2>/dev/null || true', { stdio: 'ignore' });
      }
    } catch {}
  }

  getUnprocessedTickets() {
    return this.loadQueue().filter(e => !e.processed);
  }

  markProcessed(ticketId) {
    const queue = this.loadQueue();
    const entry = queue.find(e => e.ticket.id === ticketId);
    if (entry) {
      entry.processed = true;
      entry.processedAt = new Date().toISOString();
      this.saveQueue(queue);
    }
  }
}

export default ClaudeNotifier;
