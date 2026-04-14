# API & Schema Mapping
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/migrate/api-schema-mapping



## API endpoint mapping

### Create a payment request

<Tabs>
  <Tab title="Payment Link API">
    ```bash theme={null}
    POST https://business.coinbase.com/api/v1/payment-links
    Authorization: Bearer YOUR_JWT_TOKEN
    X-Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324

    {
      "amount": "100.00",
      "currency": "USDC",
      "network": "base",
      "description": "Payment for order #12345",
      "expiresAt": "2024-12-31T23:59:59Z",
      "successRedirectUrl": "https://example.com/success",
      "failRedirectUrl": "https://example.com/failed",
      "metadata": {
        "order_id": "12345",
        "customer_id": "cust_abc123"
      }
    }
    ```
  </Tab>

  <Tab title="Checkouts API">
    ```bash theme={null}
    POST https://business.coinbase.com/api/v1/checkouts
    Authorization: Bearer YOUR_JWT_TOKEN
    X-Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324

    {
      "amount": "100.00",
      "currency": "USDC",
      "network": "base",
      "description": "Payment for order #12345",
      "expiresAt": "2024-12-31T23:59:59Z",
      "successRedirectUrl": "https://example.com/success",
      "failRedirectUrl": "https://example.com/failed",
      "metadata": {
        "order_id": "12345",
        "customer_id": "cust_abc123"
      }
    }
    ```
  </Tab>
</Tabs>

<Accordion title="Key changes">
  * Request body schema is identical — no changes required
  * Only the URL path changes from `/payment-links` to `/checkouts`
</Accordion>

### List payment requests

<Tabs>
  <Tab title="Payment Link API">
    ```bash theme={null}
    GET https://business.coinbase.com/api/v1/payment-links?pageSize=20&status=ACTIVE
    Authorization: Bearer YOUR_JWT_TOKEN
    ```
  </Tab>

  <Tab title="Checkouts API">
    ```bash theme={null}
    GET https://business.coinbase.com/api/v1/checkouts?pageSize=20&status=ACTIVE
    Authorization: Bearer YOUR_JWT_TOKEN
    ```
  </Tab>
</Tabs>

<Accordion title="Key changes">
  * Response key changes from `paymentLinks` to `checkouts`
  * Pagination (`pageSize`, `pageToken`, `nextPageToken`) is unchanged
  * Status filter values are unchanged
</Accordion>

### Retrieve a specific payment request

<Tabs>
  <Tab title="Payment Link API">
    ```bash theme={null}
    GET https://business.coinbase.com/api/v1/payment-links/{paymentLinkId}
    Authorization: Bearer YOUR_JWT_TOKEN
    ```
  </Tab>

  <Tab title="Checkouts API">
    ```bash theme={null}
    GET https://business.coinbase.com/api/v1/checkouts/{id}
    Authorization: Bearer YOUR_JWT_TOKEN
    ```
  </Tab>
</Tabs>

<Accordion title="Key changes">
  * Path parameter renamed from `paymentLinkId` to `id`
  * ID format (24-character hexadecimal) is unchanged
</Accordion>

### Deactivate a payment request

<Tabs>
  <Tab title="Payment Link API">
    ```bash theme={null}
    POST https://business.coinbase.com/api/v1/payment-links/{paymentLinkId}/deactivate
    Authorization: Bearer YOUR_JWT_TOKEN
    ```
  </Tab>

  <Tab title="Checkouts API">
    ```bash theme={null}
    POST https://business.coinbase.com/api/v1/checkouts/{id}/deactivate
    Authorization: Bearer YOUR_JWT_TOKEN
    ```
  </Tab>
</Tabs>

<Accordion title="Key changes">
  * Path parameter renamed from `paymentLinkId` to `id`
  * Behavior is identical — only `ACTIVE` resources can be deactivated
</Accordion>

## Response schema mapping

### Payment details

| Payment Link API Field | Checkouts API Field  | Notes                                                                     |
| :--------------------- | :------------------- | :------------------------------------------------------------------------ |
| `id`                   | `id`                 | Same format (24-character hexadecimal)                                    |
| `url`                  | `url`                | Same purpose                                                              |
| `status`               | `status`             | Same values (ACTIVE, PROCESSING, DEACTIVATED, EXPIRED, COMPLETED, FAILED) |
| `amount`               | `amount`             | Unchanged                                                                 |
| `currency`             | `currency`           | Unchanged                                                                 |
| `network`              | `network`            | Unchanged                                                                 |
| `address`              | `address`            | Unchanged                                                                 |
| `tokenAddress`         | `tokenAddress`       | Unchanged                                                                 |
| `description`          | `description`        | Unchanged                                                                 |
| `metadata`             | `metadata`           | Unchanged                                                                 |
| `expiresAt`            | `expiresAt`          | Unchanged                                                                 |
| `successRedirectUrl`   | `successRedirectUrl` | Unchanged                                                                 |
| `failRedirectUrl`      | `failRedirectUrl`    | Unchanged                                                                 |
| `createdAt`            | `createdAt`          | Unchanged                                                                 |
| `updatedAt`            | `updatedAt`          | Unchanged                                                                 |
| `settlement`           | `settlement`         | Unchanged                                                                 |
| `transactionHash`      | `transactionHash`    | Unchanged                                                                 |

## Webhook event mapping

### Updating your subscriptions

<Tabs>
  <Tab title="Payment Link API subscription">
    ```bash theme={null}
    cdpcurl -X POST \
      -i "YOUR_API_KEY_ID" \
      -s "YOUR_API_KEY_SECRET" \
      "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
      -d '{
        "description": "Payment link status webhook",
        "eventTypes": [
          "payment_link.payment.success",
          "payment_link.payment.failed",
          "payment_link.payment.expired"
        ],
        "target": {
          "url": "https://your-webhook-url.com",
          "method": "POST"
        },
        "isEnabled": true
      }'
    ```
  </Tab>

  <Tab title="Checkouts API subscription">
    ```bash theme={null}
    cdpcurl -X POST \
      -i "YOUR_API_KEY_ID" \
      -s "YOUR_API_KEY_SECRET" \
      "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
      -d '{
        "description": "Checkout status webhook",
        "eventTypes": [
          "checkout.payment.success",
          "checkout.payment.failed",
          "checkout.payment.expired"
        ],
        "target": {
          "url": "https://your-webhook-url.com",
          "method": "POST"
        },
        "isEnabled": true
      }'
    ```
  </Tab>
</Tabs>

### Event type mapping

| Payment Link API Event         | Checkouts API Event        |
| :----------------------------- | :------------------------- |
| `payment_link.payment.success` | `checkout.payment.success` |
| `payment_link.payment.failed`  | `checkout.payment.failed`  |
| `payment_link.payment.expired` | `checkout.payment.expired` |

## Node.js implementation examples

<Tabs>
  <Tab title="Payment Link API">
    ```javascript theme={null}
    const axios = require('axios');
    const { v4: uuidv4 } = require('uuid');

    function generateBearerToken() {
      // Refer to authentication docs
      return 'YOUR_JWT_TOKEN';
    }

    async function createPaymentLink(orderData) {
      const response = await axios.post(
        'https://business.coinbase.com/api/v1/payment-links',
        {
          amount: orderData.amount,
          currency: 'USDC',
          network: 'base',
          description: orderData.description,
          successRedirectUrl: orderData.successUrl,
          failRedirectUrl: orderData.failUrl,
          metadata: orderData.metadata
        },
        {
          headers: {
            'Authorization': `Bearer ${generateBearerToken()}`,
            'Content-Type': 'application/json',
            'X-Idempotency-Key': uuidv4()
          }
        }
      );

      return {
        id: response.data.id,
        url: response.data.url,
        expiresAt: response.data.expiresAt
      };
    }

    async function getStatus(id) {
      const response = await axios.get(
        `https://business.coinbase.com/api/v1/payment-links/${id}`,
        { headers: { 'Authorization': `Bearer ${generateBearerToken()}` } }
      );
      return response.data.status;
    }
    ```
  </Tab>

  <Tab title="Checkouts API">
    ```javascript theme={null}
    const axios = require('axios');
    const { v4: uuidv4 } = require('uuid');

    function generateBearerToken() {
      // Refer to authentication docs
      return 'YOUR_JWT_TOKEN';
    }

    async function createCheckout(orderData) {
      const response = await axios.post(
        'https://business.coinbase.com/api/v1/checkouts',  // only URL changes
        {
          amount: orderData.amount,
          currency: 'USDC',
          network: 'base',
          description: orderData.description,
          successRedirectUrl: orderData.successUrl,
          failRedirectUrl: orderData.failUrl,
          metadata: orderData.metadata
        },
        {
          headers: {
            'Authorization': `Bearer ${generateBearerToken()}`,
            'Content-Type': 'application/json',
            'X-Idempotency-Key': uuidv4()
          }
        }
      );

      return {
        id: response.data.id,
        url: response.data.url,
        expiresAt: response.data.expiresAt
      };
    }

    async function getStatus(id) {
      const response = await axios.get(
        `https://business.coinbase.com/api/v1/checkouts/${id}`,  // only URL changes
        { headers: { 'Authorization': `Bearer ${generateBearerToken()}` } }
      );
      return response.data.status;
    }
    ```
  </Tab>
</Tabs>

