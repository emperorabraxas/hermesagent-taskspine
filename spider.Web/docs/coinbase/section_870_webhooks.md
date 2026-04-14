# Webhooks
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/webhooks



Checkout webhooks provide your app with real-time payment status updates. By subscribing your webhook endpoint you will receive a notification every time a checkout status changes.

## Setup

### Prerequisites

You will need:

* Your CDP API Key ID and secret
* A webhook notification HTTPS URL
* (Recommended) Install [cdpcurl](https://github.com/coinbase/cdpcurl)

### Create a webhook subscription

1. Prepare your subscription configuration:

```json theme={null}
{
  "description": "Checkout status webhook",
  "eventTypes": [
    "checkout.payment.success",
    "checkout.payment.failed",
    "checkout.payment.expired",
    "checkout.refund.success",
    "checkout.refund.failed"
  ],
  "target": {
    "url": "https://your-webhook-url.com",
    "method": "POST"
  },
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
    "method": "POST",
    "headers": {
      "custom-header": "value"
    }
},
...
```

* All Checkout event types should be included to ensure you receive notifications for every checkout state change:

| Event type                 | Description                      |
| :------------------------- | :------------------------------- |
| `checkout.payment.success` | Checkout successfully paid       |
| `checkout.payment.failed`  | Checkout payment failed          |
| `checkout.payment.expired` | Checkout expired without payment |
| `checkout.refund.success`  | Refund completed successfully    |
| `checkout.refund.failed`   | Refund failed                    |

2. Create the webhook subscription:

```bash lines wrap theme={null}
cdpcurl -X POST \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
  -d '{
    "description": "Checkout status webhook",
    "eventTypes": [
      "checkout.payment.success",
      "checkout.payment.failed",
      "checkout.payment.expired",
      "checkout.refund.success",
      "checkout.refund.failed"
    ],
    "target": {
      "url": "https://your-webhook-url.com",
      "method": "POST"
    },
    "isEnabled": true
  }'
```

Sample webhook subscription response:

```bash lines wrap theme={null}
201 Created
{
  "createdAt": "2025-09-10T13:58:38.681893Z",
  "description": "Checkout status webhook",
  "eventTypes": [
    "checkout.payment.success",
    "checkout.payment.failed",
    "checkout.payment.expired",
    "checkout.refund.success",
    "checkout.refund.failed"
  ],
  "isEnabled": true,
  "labelKey": "user_uuid",
  "labelValue": "<YOUR_USER_UUID>",
  "labels": {
    "user_uuid": "<YOUR_USER_UUID>"
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
    "description": "Updated: Checkout status webhook",
    "eventTypes": [
      "checkout.payment.success",
      "checkout.payment.failed",
      "checkout.payment.expired",
      "checkout.refund.success",
      "checkout.refund.failed"
    ],
    "target": {
      "url": "https://your-new-webhook-url.com",
      "method": "POST"
    },
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

<b>List subscription events</b>

View delivery attempts for a subscription, including delivery status, retry count, and HTTP response details:

```bash theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>/events"
```

You can narrow results with the following optional query parameters:

| Parameter        | Description                                                                                           |
| :--------------- | :---------------------------------------------------------------------------------------------------- |
| `eventId`        | Filter by a specific event ID                                                                         |
| `minCreatedAt`   | Only include events created at or after this timestamp (RFC 3339, e.g. `2025-01-15T00:00:00Z`)        |
| `maxCreatedAt`   | Only include events created at or before this timestamp (RFC 3339)                                    |
| `eventTypeNames` | Filter by event type names, comma-separated (e.g. `checkout.payment.success,checkout.payment.failed`) |

Results are limited to the 50 most recent events, returned newest first. Example with filters:

```bash lines wrap theme={null}
cdpcurl -X GET \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions/<SUBSCRIPTION_ID>/events?minCreatedAt=2025-01-15T00:00:00Z&eventTypeNames=checkout.payment.success,checkout.refund.success"
```

### Webhook signature verification

<Warning>
  Verify webhook signatures to ensure that requests are authentic. This protects your application from forged webhooks and potential security threats.
</Warning>

#### How it works

When you create a webhook subscription, the response includes a top-level `secret`. Use this value to verify that incoming webhooks are authentic.

Each webhook request includes an `X-Hook0-Signature` header containing:

* `t` field - the timestamp
* `h` field - list of headers included in the signature
* `v1` field - the signature

#### Implementation

Here's an example of how to verify webhook signatures:

```javascript Node.js lines wrap theme={null}
const crypto = require('crypto');

/**
 * Verify webhook signature and timestamp
 * @param {string} payload - Raw request body as string
 * @param {string} signatureHeader - X-Hook0-Signature header value
 * @param {string} secret - Webhook secret from the subscription response
 * @param {Object} headers - HTTP headers from webhook request
 * @param {number} maxAgeMinutes - Max age for webhook (default: 5 minutes)
 * @returns {boolean} true if webhook is authentic and within allowed time window
 */
function verifyWebhookSignature(payload, signatureHeader, secret, headers, maxAgeMinutes = 5) {
    try {
        // Parse signature header: t=timestamp,h=headers,v1=signature
        const elements = signatureHeader.split(',');
        const timestamp = elements.find(e => e.startsWith('t=')).split('=')[1];
        const headerNames = elements.find(e => e.startsWith('h=')).split('=')[1];
        const providedSignature = elements.find(e => e.startsWith('v1=')).split('=')[1];

        // Build header values string
        const headerNameList = headerNames.split(' ');
        const headerValues = headerNameList.map(name => headers[name] || '').join('.');

        // Build signed payload
        const signedPayload = `${timestamp}.${headerNames}.${headerValues}.${payload}`;

        // Compute expected signature
        const expectedSignature = crypto
            .createHmac('sha256', secret)
            .update(signedPayload, 'utf8')
            .digest('hex');

        // Compare signatures securely
        const signaturesMatch = crypto.timingSafeEqual(
            Buffer.from(expectedSignature, 'hex'),
            Buffer.from(providedSignature, 'hex')
        );

        // Verify timestamp to prevent replay attacks
        const webhookTime = parseInt(timestamp) * 1000; // Convert to milliseconds
        const currentTime = Date.now();
        const ageMinutes = (currentTime - webhookTime) / (1000 * 60);

        if (ageMinutes > maxAgeMinutes) {
            console.error(`Webhook timestamp exceeds maximum age: ${ageMinutes.toFixed(1)} minutes > ${maxAgeMinutes} minutes`);
            return false;
        }

        return signaturesMatch;

    } catch (error) {
        console.error('Webhook verification error:', error);
        return false;
    }
}
```

And in your application:

```javascript Node.js lines wrap theme={null}
const express = require("express");
const app = express();

// Important: Get raw body for signature verification
app.use(express.raw({ type: "application/json" }));

app.post("/webhook", (req, res) => {
    const payload = req.body.toString(); // Raw string needed for signature
    const signature = req.headers["x-hook0-signature"];
    const secret = process.env.WEBHOOK_SECRET; // Store securely from the subscription response

    if (verifyWebhookSignature(payload, signature, secret, req.headers)) {
        console.log("✅ Authentic webhook");

        // Parse and process the event
        const event = JSON.parse(payload);

        // Handle your checkout event here

        res.status(200).send("OK");
    } else {
        console.log("❌ Invalid webhook - rejected");
        res.status(400).send("Invalid signature");
    }
});
```

### Next steps

Once your subscription is created, your endpoint will begin receiving webhook events for checkouts!

#### Sample checkout event payloads

```json lines wrap theme={null}
// Checkout payment success event
{
  "id": "69163c762331ed43dc64a6ef",
  "url": "https://payments.coinbase.com/payment-links/pl_01k9zdrbdeezj98vaqaxrfare0",
  "amount": "100.00",
  "currency": "USDC",
  "network": "base",
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "description": "Payment for order #12345",
  "eventType": "checkout.payment.success",
  "expiresAt": "2026-12-31T23:59:59Z",
  "failRedirectUrl": "https://example.com/failed",
  "metadata": {
    "customerId": "cust_abc123",
    "orderId": "12345"
  },
  "settlement": {
    "totalAmount": "100.00",
    "feeAmount": "1.25",
    "netAmount": "98.75",
    "currency": "USDC"
  },
  "status": "COMPLETED",
  "successRedirectUrl": "https://example.com/success",
  "transactionHash": "0x3a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
  "createdAt": "2025-11-13T20:15:49.329Z",
  "updatedAt": "2025-11-13T20:16:55.097Z"
}

// Checkout payment failed event
{
  "id": "69163c762331ed43dc64a6ef",
  "url": "https://payments.coinbase.com/payment-links/pl_01k9zdrbdeezj98vaqaxrfare0",
  "amount": "100.00",
  "currency": "USDC",
  "network": "base",
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "description": "Payment for order #12345",
  "eventType": "checkout.payment.failed",
  "expiresAt": "2026-12-31T23:59:59Z",
  "failRedirectUrl": "https://example.com/failed",
  "metadata": {
    "customerId": "cust_abc123",
    "orderId": "12345"
  },
  "status": "FAILED",
  "createdAt": "2025-11-13T20:15:49.329Z",
  "updatedAt": "2025-11-13T20:15:49.329Z"
}

// Checkout payment expired event
{
  "id": "69163c762331ed43dc64a6ef",
  "url": "https://payments.coinbase.com/payment-links/pl_01k9zdrbdeezj98vaqaxrfare0",
  "amount": "100.00",
  "currency": "USDC",
  "network": "base",
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "description": "Payment for order #12345",
  "eventType": "checkout.payment.expired",
  "expiresAt": "2025-11-13T20:15:49.329Z",
  "metadata": {
    "customerId": "cust_abc123",
    "orderId": "12345"
  },
  "status": "EXPIRED",
  "createdAt": "2025-11-01T10:00:00.000Z",
  "updatedAt": "2025-11-13T20:15:49.329Z"
}

// Checkout refund success event
{
  "id": "69163c762331ed43dc64a6ef",
  "url": "https://payments.coinbase.com/payment-links/pl_01k9zdrbdeezj98vaqaxrfare0",
  "amount": "100.00",
  "currency": "USDC",
  "network": "base",
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "description": "Payment for order #12345",
  "eventType": "checkout.refund.success",
  "metadata": {
    "customerId": "cust_abc123",
    "orderId": "12345"
  },
  "settlement": {
    "totalAmount": "100.00",
    "feeAmount": "1.25",
    "netAmount": "98.75",
    "currency": "USDC"
  },
  "status": "REFUNDED",
  "refundedAmount": "100.00",
  "refunds": [
    {
      "id": "69163c762331ed43dc64b7fg",
      "checkoutId": "69163c762331ed43dc64a6ef",
      "amount": "100.00",
      "currency": "USDC",
      "status": "COMPLETED",
      "reason": "Customer requested refund",
      "transactionHash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
      "createdAt": "2025-11-14T10:00:00.000Z",
      "completedAt": "2025-11-14T10:05:00.000Z"
    }
  ],
  "transactionHash": "0x3a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
  "createdAt": "2025-11-13T20:15:49.329Z",
  "updatedAt": "2025-11-14T10:05:00.000Z"
}

```

