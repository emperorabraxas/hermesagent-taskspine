# Update webhook subscription
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/webhooks-under-development/update-webhook-subscription

put /v2/data/webhooks/subscriptions/{subscriptionId}
Update an existing webhook subscription's configuration including
event types, target URL, filtering criteria, and enabled status.
All required fields must be provided, even if they are not being changed.

### Common Updates
- Change target URL or headers
- Add/remove event type filters
- Update multi-label filtering criteria
- Enable/disable subscription



