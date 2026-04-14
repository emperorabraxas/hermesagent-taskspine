# Delete webhook subscription
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/webhooks-under-development/delete-webhook-subscription

delete /v2/data/webhooks/subscriptions/{subscriptionId}
Permanently delete a webhook subscription and stop all event deliveries.
This action cannot be undone.

### Important Notes
- All webhook deliveries will cease immediately
- Subscription cannot be recovered after deletion
- Consider disabling instead of deleting for temporary pauses



