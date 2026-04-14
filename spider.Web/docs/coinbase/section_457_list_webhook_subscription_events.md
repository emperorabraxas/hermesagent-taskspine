# List webhook subscription events
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/webhooks/list-webhook-subscription-events

get /v2/data/webhooks/subscriptions/{subscriptionId}/events
Retrieve webhook event delivery attempts for a specific subscription.
Returns event deliveries in descending order by creation time (newest first),
including delivery status, retry count, and response details.

### Use Cases
- Debug webhook delivery failures and inspect response codes
- Monitor delivery status and retry counts
- Audit event delivery history for a subscription
- Verify that expected events were sent to webhook URLs

### Filtering
Use optional query parameters to narrow results:
- `eventId` — find a specific event by ID
- `minCreatedAt` / `maxCreatedAt` — filter by time range
- `eventTypeNames` — filter by event type (comma-separated)

**Note:** Results are limited to the 50 most recent events (newest first). No pagination is supported.



