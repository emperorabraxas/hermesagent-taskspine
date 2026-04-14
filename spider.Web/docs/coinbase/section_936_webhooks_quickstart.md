# Webhooks Quickstart
Source: https://docs.cdp.coinbase.com/data/webhooks/quickstart



## Overview

Get started with Onchain Webhooks in just a few steps. This guide will help you create a webhook subscription via our [REST endpoints](/api-reference/v2/rest-api/webhooks/webhooks) and receive the events at a target destination.

## Prerequisites

<AccordionGroup>
  <Accordion title="A Secret API Key">
    Sign up at [portal.cdp.coinbase.com](https://portal.cdp.coinbase.com), then navigate to [API Keys](https://portal.cdp.coinbase.com/projects/api-keys) and select **Create API key** under the **Secret API Keys** tab.

    1. Enter an API key nickname (restrictions are optional)
    2. Click **Create**
    3. Secure your API Key ID and Secret in a safe location
  </Accordion>

  <Accordion title="A webhook URL">
    You'll need an HTTPS URL to receive webhook events. For quick testing, [webhook.site](https://webhook.site) gives free temporary URLs instantly.

    For production, use your own HTTPS endpoint.
  </Accordion>

  <Accordion title="cdpcurl">
    Install `cdpcurl` to make authenticated requests to CDP APIs:

    ```bash theme={null}
    # With Homebrew
    brew tap coinbase/cdpcurl && brew install cdpcurl

    # Or with Go
    go install github.com/coinbase/cdpcurl@latest
    ```
  </Accordion>
</AccordionGroup>

## 1. Construct subscription payload

Create a JSON payload to be used with `cdpcurl` in the next step:

```json title="subscription.json" theme={null}
{
  "description": "USD Base Coin Transfers",
  "eventTypes": [
    "onchain.activity.detected",
  ],
  "target": {
    "url": "https://your-webhook-url.com",
    "method": "POST"
  },
  "labels": {
    "contract_address": "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca", # USD Base Coin Contract Address
    "event_name": "Transfer",
  },
  "isEnabled": true
}
```

### Configuration fields

Below is a list of all payload information that can be provided when creating a webhook subscription:

| Field                       | Description                                          | Required                          | Notes                                                                                                                     |
| --------------------------- | ---------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `target.url`                | Your webhook endpoint URL                            | Yes                               | Must be a valid HTTPS URL                                                                                                 |
| `labels.contract_address`   | Smart contract address to monitor                    | Yes                               | Hex address with `0x` prefix                                                                                              |
| `labels.event_name`         | Smart contract event name                            | Yes\* (this OR `event_signature`) | Event name from ABI (e.g., `Transfer`)                                                                                    |
| `labels.event_signature`    | Smart contract event signature                       | Yes\* (this OR `event_name`)      | Full signature (e.g., `Transfer(address,address,uint256)`)                                                                |
| `eventTypes`                | Array of event types                                 | No                                | Use `["onchain.activity.detected"]` if provided                                                                           |
| `isEnabled`                 | Enable/disable webhook                               | No                                | Defaults to `true`                                                                                                        |
| `target.headers`            | Custom HTTP headers                                  | No                                | Object with header key-value pairs                                                                                        |
| `labels.transaction_from`   | Transaction source address                           | No                                |                                                                                                                           |
| `labels.transaction_to`     | Transaction destination address                      | No                                |                                                                                                                           |
| `labels.network`            | Network name (e.g. `base-mainnet` or `base-sepolia`) | No                                | Defaults to `base-mainnet`                                                                                                |
| `labels.params.[any_param]` | Any smart contract parameter                         | No                                | Add any parameter from the contract event for hyper-granular filtering (e.g., `params.from`, `params.to`, `params.value`) |

### Custom headers

You can also set a `headers` object in `target` if your URL requires specific headers:

```json title="custom-headers.json" theme={null}
"target": {
    "url": "https://your-webhook-url.com",
    "method": "POST",
    "headers": {
      "custom-header": "value"
    }
},
```

## 2. Create subscription

Using the configuration you created in the previous step, create the webhook subscription using `cdpcurl`:

```bash lines theme={null}
cdpcurl -X POST \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
  -d '{
  "description": "USD Base Coin Transfers",
  "eventTypes": [
    "onchain.activity.detected",
  ],
  "target": {
    "url": "https://your-webhook-url.com",
    "method": "POST"
  },
  "labels": {
    "contract_address": "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca", # USD Base Coin Contract Address
    "event_name": "Transfer",
  },
  "isEnabled": true
}'
```

You should see a response similar to the following:

```json title="response.json" theme={null}
201 Created
{
  "createdAt": "2025-10-08T13:58:38.681893Z",
  "description": "USD Base Coin Transfers",
  "eventTypes": [
    "onchain.activity.detected"
  ],
  "isEnabled": true,
  "labels": {
    "project": "<YOUR_CDP_PROJECT_ID>",
    "contract_address": "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca", # USD Base Coin Contract Address
    "event_name": "Transfer",
  },
  "metadata": {
    "secret": "<SECRET_FOR_WEBHOOK_VERIFICATION>"
  },
  "subscriptionId": "<YOUR_SUBSCRIPTION_ID>",
  "target": {
    "url": "https://your-webhook-url.com"
  }
}
```

## Additional endpoints

See the following examples to view, update, or delete the subscription using the `subscriptionId` from the response.

### List all subscriptions

```bash theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions"
```

### View subscription details

```bash theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>"
```

### Update subscription

```bash theme={null}
cdpcurl -X PUT \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>" \
  -d '{
    "description": "Updated: USD Base Coin Transfers",
    "eventTypes": [
    "onchain.activity.detected",
    ],
    "target": {
      "url": "https://your-webhook-url.com",
      "method": "POST"
    },
    "labels": {},
    "isEnabled": true
  }'
```

### Delete subscription

```bash theme={null}
cdpcurl -X DELETE \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>"
```

### List subscription events

View delivery attempts for a subscription, including delivery status, retry count, and HTTP response details:

```bash theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>/events"
```

You can narrow results with the following optional query parameters:

| Parameter        | Description                                                                                    |
| :--------------- | :--------------------------------------------------------------------------------------------- |
| `eventId`        | Filter by a specific event ID                                                                  |
| `minCreatedAt`   | Only include events created at or after this timestamp (RFC 3339, e.g. `2025-01-15T00:00:00Z`) |
| `maxCreatedAt`   | Only include events created at or before this timestamp (RFC 3339)                             |
| `eventTypeNames` | Filter by event type names, comma-separated (e.g. `onchain.activity.detected`)                 |

Results are limited to the 50 most recent events, returned newest first. Example with filters:

```bash lines wrap theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>/events?minCreatedAt=2025-01-15T00:00:00Z&eventTypeNames=onchain.activity.detected"
```

## What to read next

* **[Verify webhook signatures](/data/webhooks/verify-signatures)**: Learn how to verify webhook signatures to ensure events are coming from Coinbase
* **<a href="/api-reference/v2/rest-api/webhooks/webhooks">REST API Reference</a>**: View the complete webhook API documentation
* **[Support](/support/join-cdp-discord)**: Join our Discord for help and community support

