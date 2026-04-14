# Get webhook subscription details
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/webhooks/get-webhook-subscription-details

get /v2/data/webhooks/subscriptions/{subscriptionId}
Retrieve detailed information about a specific webhook subscription including
configuration, status, creation timestamp, and webhook signature secret.

### Response Includes
- Subscription configuration and filters
- Target URL and custom headers
- Webhook signature secret for verification
- Creation timestamp and status



