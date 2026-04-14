# List webhook subscriptions
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/webhooks-under-development/list-webhook-subscriptions

get /v2/data/webhooks/subscriptions
Retrieve a paginated list of webhook subscriptions for the authenticated project.
Returns subscriptions for all CDP product events (onchain, onramp/offramp, wallet, etc.)
in descending order by creation time.

### Use Cases
- Monitor all active webhook subscriptions across CDP products
- Audit webhook configurations
- Manage subscription lifecycle



