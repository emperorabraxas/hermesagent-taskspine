#!/usr/bin/env node
import 'dotenv/config';
import { FreshdeskClient } from '../src/freshdesk-client.js';
import { createServer } from 'http';
import { readFileSync } from 'fs';

const domain = process.env.FRESHDESK_DOMAIN;
const apiKey = process.env.FRESHDESK_API_KEY;

if (!domain || !apiKey) {
  console.error('Missing FRESHDESK_DOMAIN or FRESHDESK_API_KEY');
  process.exit(1);
}

const client = new FreshdeskClient(domain, apiKey);

const tools = {
  list_tickets: {
    description: 'List recent support tickets from Freshdesk',
    inputSchema: {
      type: 'object',
      properties: {
        filter: {
          type: 'string',
          enum: ['new_and_my_open', 'watching', 'spam', 'deleted'],
          description: 'Ticket filter'
        },
        limit: { type: 'number', description: 'Max tickets to return (default 10)' }
      }
    },
    handler: async (params) => {
      const tickets = await client.listTickets({ filter: params.filter });
      const limited = tickets.slice(0, params.limit || 10);
      return limited.map(t => client.formatTicketForClaude(t));
    }
  },

  get_ticket: {
    description: 'Get full details of a specific ticket including conversation history',
    inputSchema: {
      type: 'object',
      properties: {
        ticket_id: { type: 'number', description: 'The ticket ID' }
      },
      required: ['ticket_id']
    },
    handler: async (params) => {
      const ticket = await client.getTicket(params.ticket_id);
      return client.formatTicketForClaude(ticket);
    }
  },

  add_private_note: {
    description: 'Add a private internal note to a ticket (not visible to customer)',
    inputSchema: {
      type: 'object',
      properties: {
        ticket_id: { type: 'number', description: 'The ticket ID' },
        note: { type: 'string', description: 'The note content' }
      },
      required: ['ticket_id', 'note']
    },
    handler: async (params) => {
      await client.addNote(params.ticket_id, params.note, true);
      return { success: true, message: 'Private note added' };
    }
  },

  reply_to_ticket: {
    description: 'Send a reply to the customer on a ticket',
    inputSchema: {
      type: 'object',
      properties: {
        ticket_id: { type: 'number', description: 'The ticket ID' },
        message: { type: 'string', description: 'The reply message' }
      },
      required: ['ticket_id', 'message']
    },
    handler: async (params) => {
      await client.replyToTicket(params.ticket_id, params.message);
      return { success: true, message: 'Reply sent to customer' };
    }
  },

  update_ticket_status: {
    description: 'Update the status of a ticket',
    inputSchema: {
      type: 'object',
      properties: {
        ticket_id: { type: 'number', description: 'The ticket ID' },
        status: {
          type: 'number',
          enum: [2, 3, 4, 5],
          description: '2=Open, 3=Pending, 4=Resolved, 5=Closed'
        },
        priority: {
          type: 'number',
          enum: [1, 2, 3, 4],
          description: '1=Low, 2=Medium, 3=High, 4=Urgent'
        }
      },
      required: ['ticket_id']
    },
    handler: async (params) => {
      const updates = {};
      if (params.status) updates.status = params.status;
      if (params.priority) updates.priority = params.priority;
      await client.updateTicket(params.ticket_id, updates);
      return { success: true, message: 'Ticket updated' };
    }
  },

  get_new_tickets: {
    description: 'Get tickets created or updated in the last N minutes',
    inputSchema: {
      type: 'object',
      properties: {
        minutes: { type: 'number', description: 'Look back this many minutes (default 30)' }
      }
    },
    handler: async (params) => {
      const tickets = await client.getNewOrUpdatedTickets(params.minutes || 30);
      return tickets.map(t => client.formatTicketForClaude(t));
    }
  },

  check_ticket_queue: {
    description: 'Check for tickets queued by the auto-handler for this session',
    inputSchema: {
      type: 'object',
      properties: {
        clear: { type: 'boolean', description: 'Clear queue after reading (default true)' }
      }
    },
    handler: async (params) => {
      const fs = await import('fs');
      const queueFile = process.env.CLAUDE_SESSION_FILE || '/tmp/claude-ticket-queue.json';

      if (!fs.existsSync(queueFile)) {
        return { tickets: [], message: 'No tickets in queue' };
      }

      try {
        const queue = JSON.parse(fs.readFileSync(queueFile, 'utf8'));

        if (params.clear !== false && queue.length > 0) {
          fs.writeFileSync(queueFile, '[]');
        }

        return {
          tickets: queue,
          count: queue.length,
          message: queue.length > 0
            ? `${queue.length} ticket(s) ready for review`
            : 'No tickets in queue'
        };
      } catch (e) {
        return { tickets: [], error: e.message };
      }
    }
  }
};

async function handleMcpRequest(request) {
  const { method, params, id } = request;

  if (method === 'initialize') {
    return {
      jsonrpc: '2.0',
      id,
      result: {
        protocolVersion: '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: { name: 'freshdesk-mcp', version: '1.0.0' }
      }
    };
  }

  if (method === 'tools/list') {
    return {
      jsonrpc: '2.0',
      id,
      result: {
        tools: Object.entries(tools).map(([name, def]) => ({
          name,
          description: def.description,
          inputSchema: def.inputSchema
        }))
      }
    };
  }

  if (method === 'tools/call') {
    const { name, arguments: args } = params;
    const tool = tools[name];

    if (!tool) {
      return {
        jsonrpc: '2.0',
        id,
        error: { code: -32601, message: `Unknown tool: ${name}` }
      };
    }

    try {
      const result = await tool.handler(args || {});
      return {
        jsonrpc: '2.0',
        id,
        result: { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] }
      };
    } catch (error) {
      return {
        jsonrpc: '2.0',
        id,
        error: { code: -32000, message: error.message }
      };
    }
  }

  return {
    jsonrpc: '2.0',
    id,
    error: { code: -32601, message: `Method not found: ${method}` }
  };
}

let buffer = '';
process.stdin.setEncoding('utf8');

process.stdin.on('data', async (chunk) => {
  buffer += chunk;

  const lines = buffer.split('\n');
  buffer = lines.pop();

  for (const line of lines) {
    if (!line.trim()) continue;

    try {
      const request = JSON.parse(line);
      const response = await handleMcpRequest(request);
      process.stdout.write(JSON.stringify(response) + '\n');
    } catch (error) {
      console.error('Parse error:', error.message);
    }
  }
});

process.stderr.write('Freshdesk MCP server started\n');
