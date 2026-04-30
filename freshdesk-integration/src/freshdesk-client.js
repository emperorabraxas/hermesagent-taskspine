import axios from 'axios';

export class FreshdeskClient {
  constructor(domain, apiKey) {
    this.baseUrl = `https://${domain}/api/v2`;
    this.auth = Buffer.from(`${apiKey}:X`).toString('base64');
    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Authorization': `Basic ${this.auth}`,
        'Content-Type': 'application/json'
      }
    });
  }

  async listTickets(options = {}) {
    const params = new URLSearchParams();
    if (options.filter) params.append('filter', options.filter);
    if (options.orderBy) params.append('order_by', options.orderBy);
    if (options.orderType) params.append('order_type', options.orderType);
    if (options.updatedSince) params.append('updated_since', options.updatedSince);

    const query = params.toString() ? `?${params}` : '';
    const response = await this.client.get(`/tickets${query}`);
    return response.data;
  }

  async getTicket(ticketId, include = 'conversations,requester') {
    const response = await this.client.get(`/tickets/${ticketId}?include=${include}`);
    return response.data;
  }

  async getNewOrUpdatedTickets(sinceMinutes = 5) {
    const since = new Date(Date.now() - sinceMinutes * 60 * 1000).toISOString();
    return this.listTickets({
      updatedSince: since,
      orderBy: 'updated_at',
      orderType: 'desc'
    });
  }

  async addNote(ticketId, body, isPrivate = true) {
    const response = await this.client.post(`/tickets/${ticketId}/notes`, {
      body,
      private: isPrivate
    });
    return response.data;
  }

  async replyToTicket(ticketId, body) {
    const response = await this.client.post(`/tickets/${ticketId}/reply`, {
      body
    });
    return response.data;
  }

  async updateTicket(ticketId, updates) {
    const response = await this.client.put(`/tickets/${ticketId}`, updates);
    return response.data;
  }

  formatTicketForClaude(ticket) {
    const priorityMap = { 1: 'Low', 2: 'Medium', 3: 'High', 4: 'Urgent' };
    const statusMap = { 2: 'Open', 3: 'Pending', 4: 'Resolved', 5: 'Closed' };

    return {
      id: ticket.id,
      subject: ticket.subject,
      description: this.stripHtml(ticket.description_text || ticket.description),
      priority: priorityMap[ticket.priority] || 'Unknown',
      status: statusMap[ticket.status] || 'Unknown',
      requester: ticket.requester?.name || ticket.requester_id,
      requesterEmail: ticket.requester?.email,
      createdAt: ticket.created_at,
      updatedAt: ticket.updated_at,
      tags: ticket.tags || [],
      conversations: (ticket.conversations || []).map(c => ({
        from: c.from_email,
        body: this.stripHtml(c.body_text || c.body),
        createdAt: c.created_at,
        incoming: c.incoming
      }))
    };
  }

  stripHtml(html) {
    if (!html) return '';
    return html
      .replace(/<[^>]*>/g, '')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }
}

export default FreshdeskClient;
