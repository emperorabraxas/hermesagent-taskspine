#!/usr/bin/env node
import 'dotenv/config';
import { FreshdeskClient } from './freshdesk-client.js';

const client = new FreshdeskClient(
  process.env.FRESHDESK_DOMAIN,
  process.env.FRESHDESK_API_KEY
);

console.log('Testing Freshdesk connection...');

try {
  const tickets = await client.listTickets();
  console.log(`✓ Connected! Found ${tickets.length} ticket(s)`);
  if (tickets.length > 0) {
    console.log('\nRecent tickets:');
    tickets.slice(0, 3).forEach(t => {
      console.log(`  #${t.id}: ${t.subject}`);
    });
  }
} catch (error) {
  if (error.response?.status === 401) {
    console.error('✗ Auth failed - check your API key');
  } else {
    console.error('✗ Error:', error.message);
  }
}
