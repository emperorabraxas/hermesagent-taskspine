# Subscriptions
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/webhooks/subscriptions



Create and manage webhook subscriptions for transfer lifecycle events.

## Prerequisites

You will need:

* Your CDP API Key ID and secret
* A webhook notification HTTPS URL
* (Recommended) Install [cdpcurl](https://github.com/coinbase/cdpcurl)

## 1. Prepare payload

Define which transfer events to receive and where webhooks should be delivered.

```json theme={null}
{
  "description": "CDP Transfers webhook",
  "eventTypes": [
    "payments.transfers.quoted",
    "payments.transfers.processing",
    "payments.transfers.completed",
    "payments.transfers.failed"
  ],
  "target": {
    "url": "https://your-webhook-url.com"
  },
  "labels": {},
  "isEnabled": true
}
```

Important configuration notes:

* `target.url` should be your webhook endpoint that will receive the events
* You can also set a `headers` object in `target` if your url requires specific headers:

```json theme={null}
...
"target": {
    "url": "https://your-webhook-url.com",
    "headers": {
      "custom-header": "value"
    }
},
...
```

* All Transfer event types should be included to ensure you receive notifications for every transfer state change:

| Event type                      | Description                                 |
| :------------------------------ | :------------------------------------------ |
| `payments.transfers.quoted`     | Transfer has been quoted with fee breakdown |
| `payments.transfers.processing` | Transfer is being executed                  |
| `payments.transfers.completed`  | Transfer completed successfully             |
| `payments.transfers.failed`     | Transfer failed                             |

## 2. Subscribe

Send the payload to create the subscription, then store the returned `subscriptionId` and `secret`.

```bash lines wrap theme={null}
cdpcurl -X POST \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
  -d '{
    "description": "CDP Transfers webhook",
    "eventTypes": [
      "payments.transfers.quoted",
      "payments.transfers.processing",
      "payments.transfers.completed",
      "payments.transfers.failed"
    ],
    "target": {
      "url": "https://your-webhook-url.com"
    },
    "labels": {},
    "isEnabled": true
  }'
```

Sample webhook subscription response:

```bash lines wrap theme={null}
201 Created
{
  "createdAt": "2025-09-10T13:58:38.681893Z",
  "description": "CDP Transfers webhook",
  "eventTypes": [
    "payments.transfers.quoted",
    "payments.transfers.processing",
    "payments.transfers.completed",
    "payments.transfers.failed"
  ],
  "isEnabled": true,
  "labels": {
    "entity": "<YOUR_ENTITY_ID>"
  },
  "secret": "<SECRET_FOR_WEBHOOK_VERIFICATION>",
  "subscriptionId": "<YOUR_SUBSCRIPTION_ID>",
  "target": {
    "url": "https://your-webhook-url.com"
  }
}
```

## Manage subscriptions

Once you've created the webhook subscription, you can use the `subscriptionId` from the response to view, update, or delete the subscription.

<b>List all subscriptions</b>

```bash theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions"
```

<b>View specified subscription details by subscription ID</b>

```bash theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>"
```

<b>Update subscription</b>

```bash theme={null}
cdpcurl -X PUT \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>" \
  -d '{
    "description": "Updated: CDP Transfers webhook",
    "eventTypes": [
      "payments.transfers.quoted",
      "payments.transfers.processing",
      "payments.transfers.completed",
      "payments.transfers.failed"
    ],
    "target": {
      "url": "https://your-new-webhook-url.com"
    },
    "labels": {},
    "isEnabled": true
  }'
```

<b>Delete subscription</b>

```bash theme={null}
cdpcurl -X DELETE \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>"
```

