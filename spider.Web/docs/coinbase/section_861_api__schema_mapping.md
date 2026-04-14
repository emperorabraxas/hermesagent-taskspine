# API & Schema Mapping
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/migrate-from-commerce/api-schema-mapping



## API endpoint mapping

### Create a payment request

<Tabs>
  <Tab title="Charge API">
    ```bash theme={null}
    POST https://api.commerce.coinbase.com/charges
    X-CC-Api-Key: YOUR_API_KEY

    {
      "name": "Order #12345",
      "description": "Payment for order #12345",
      "pricing_type": "fixed_price",
      "local_price": {
        "amount": "100.00",
        "currency": "USD"
      },
      "redirect_url": "https://example.com/success",
      "cancel_url": "https://example.com/cancel",
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
  * Amount is now a direct string field (not nested in `local_price`)
  * Currency is specified directly (Checkouts API currently supports USDC)
  * Network specification is now explicit (defaults to `base`)
  * Redirect URLs have been renamed for clarity
  * `name` field is removed; use `description` instead
  * Idempotency is supported via `X-Idempotency-Key` header
</Accordion>

### List payment requests

<Tabs>
  <Tab title="Charge API">
    ```bash theme={null}
    GET https://api.commerce.coinbase.com/charges
    X-CC-Api-Key: YOUR_API_KEY
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
  * Pagination uses `pageSize` and `pageToken` instead of Commerce's cursor-based approach
  * Can filter by status (ACTIVE, PROCESSING, DEACTIVATED, EXPIRED, COMPLETED, FAILED)
  * Response includes `nextPageToken` for retrieving next page
  * Response key is `checkouts` (not `data`)
</Accordion>

### Retrieve a specific payment request

<Tabs>
  <Tab title="Charge API">
    ```bash theme={null}
    GET https://api.commerce.coinbase.com/charges/{charge_code_or_charge_id}
    X-CC-Api-Key: YOUR_API_KEY
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
  * Use the checkout ID (24-character hexadecimal format)
  * No support for retrieval by code (use ID only)
</Accordion>

### Cancel/deactivate a payment request

<Tabs>
  <Tab title="Charge API">
    ```
    No explicit endpoint available
    - Charges expire based on expires_at timestamp
    - Cannot manually cancel active charges
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
  * Explicit deactivation endpoint available
  * Deactivated checkouts cannot accept further payments
  * Status changes to `DEACTIVATED`
</Accordion>

## Response schema mapping

### Payment details

| Charge API Field         | Checkouts API Field  | Notes                                                                     |
| :----------------------- | :------------------- | :------------------------------------------------------------------------ |
| `id`                     | `id`                 | Format changed from UUID to 24-character hexadecimal                      |
| `code`                   | N/A                  | Code not available in Checkouts API                                       |
| `hosted_url`             | `url`                | The shareable payment URL                                                 |
| `name`                   | `description`        | Name field replaced by description                                        |
| `description`            | `description`        | Same purpose                                                              |
| `pricing.local.amount`   | `amount`             | Flattened structure                                                       |
| `pricing.local.currency` | `currency`           | Flattened structure                                                       |
| N/A                      | `network`            | New field specifying blockchain network                                   |
| N/A                      | `address`            | New — merchant's blockchain receiving address                             |
| N/A                      | `updatedAt`          | New — timestamp of last status update                                     |
| N/A                      | `settlement`         | New — fee breakdown (`totalAmount`, `feeAmount`, `netAmount`, `currency`) |
| N/A                      | `transactionHash`    | New — on-chain transaction hash (present when `COMPLETED`)                |
| `expires_at`             | `expiresAt`          | Same purpose, RFC 3339 format                                             |
| `metadata`               | `metadata`           | Same purpose                                                              |
| `redirect_url`           | `successRedirectUrl` | Renamed for clarity                                                       |
| `cancel_url`             | `failRedirectUrl`    | Renamed for clarity                                                       |
| `created_at`             | `createdAt`          | Same purpose, RFC 3339 format                                             |
| `timeline`               | `status`             | Status now a single field instead of timeline array                       |
| `web3_data`              | `transactionHash`    | Transaction hash available directly on the response                       |

## Status mapping

Understanding status transitions is crucial for order fulfillment:

| Charge API Status | Checkouts API Status | Description                                           |
| :---------------- | :------------------- | :---------------------------------------------------- |
| NEW               | ACTIVE               | Payment request is active and awaiting payment        |
| SIGNED            | ACTIVE               | In Checkouts, signing happens within the payment flow |
| PENDING           | PROCESSING           | Payment detected, awaiting confirmation               |
| COMPLETED         | COMPLETED            | Payment confirmed and finalized                       |
| EXPIRED           | EXPIRED              | Payment request expired without payment               |
| FAILED            | FAILED               | Payment attempt failed                                |
| N/A               | DEACTIVATED          | Checkout manually deactivated                         |

<Note>
  **Important considerations:**

  * Checkouts API focuses on the checkout status, not individual transaction status
  * Use webhooks for real-time payment status notifications (see [Webhooks documentation](/coinbase-business/checkout-apis/webhooks))
  * Once a payment is detected and confirmed, the status changes to `COMPLETED`
</Note>

## Webhooks

### Charge API webhooks

Commerce provides webhook events:

* `charge:created`
* `charge:pending`
* `charge:confirmed`
* `charge:failed`

### Checkouts API webhooks

Checkouts API supports webhooks for real-time payment notifications:

* `checkout.payment.success` - Checkout successfully paid
* `checkout.payment.failed` - Checkout payment failed
* `checkout.payment.expired` - Checkout expired without payment

See the [Webhooks documentation](/coinbase-business/checkout-apis/webhooks) for detailed setup instructions, including:

* Creating webhook subscriptions using CDP API
* Webhook signature verification
* Sample event payloads

<Note>
  If you prefer not to use webhooks, you can also monitor payment status by periodically polling the GET endpoint to check checkout status.
</Note>

## Node.js implementation examples

<Tabs>
  <Tab title="Charge API">
    ```javascript theme={null}
    const axios = require('axios');

    async function createCharge(orderData) {
      const response = await axios.post(
        'https://api.commerce.coinbase.com/charges',
        {
          name: orderData.name,
          description: orderData.description,
          pricing_type: 'fixed_price',
          local_price: {
            amount: orderData.amount,
            currency: 'USD'
          },
          redirect_url: orderData.successUrl,
          cancel_url: orderData.cancelUrl,
          metadata: orderData.metadata
        },
        {
          headers: {
            'X-CC-Api-Key': process.env.COMMERCE_API_KEY,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        id: response.data.id,
        hostedUrl: response.data.hosted_url,
        expiresAt: response.data.expires_at
      };
    }

    async function getChargeStatus(chargeId) {
      const response = await axios.get(
        `https://api.commerce.coinbase.com/charges/${chargeId}`,
        {
          headers: {
            'X-CC-Api-Key': process.env.COMMERCE_API_KEY
          }
        }
      );

      const timeline = response.data.timeline;
      const currentStatus = timeline[timeline.length - 1].status;

      return currentStatus;
    }
    ```
  </Tab>

  <Tab title="Checkouts API">
    ```javascript theme={null}
    const axios = require('axios');
    const { v4: uuidv4 } = require('uuid');

    // Helper function to generate JWT bearer token
    // See: https://docs.cdp.coinbase.com/api-reference/v2/authentication
    function generateBearerToken() {
      // Implementation depends on your CDP API key setup
      // This is a placeholder - refer to authentication docs
      return 'YOUR_JWT_TOKEN';
    }

    async function createCheckout(orderData) {
      const bearerToken = generateBearerToken();
      const idempotencyKey = uuidv4();

      const response = await axios.post(
        'https://business.coinbase.com/api/v1/checkouts',
        {
          amount: orderData.amount,
          currency: 'USDC',
          network: 'base',
          description: orderData.description,
          expiresAt: new Date(Date.now() + 60 * 60 * 1000).toISOString(), // 1 hour
          successRedirectUrl: orderData.successUrl,
          failRedirectUrl: orderData.failUrl,
          metadata: orderData.metadata
        },
        {
          headers: {
            'Authorization': `Bearer ${bearerToken}`,
            'Content-Type': 'application/json',
            'X-Idempotency-Key': idempotencyKey
          }
        }
      );

      return {
        id: response.data.id,
        url: response.data.url,
        address: response.data.address,
        expiresAt: response.data.expiresAt
      };
    }

    async function getCheckoutStatus(id) {
      const bearerToken = generateBearerToken();

      const response = await axios.get(
        `https://business.coinbase.com/api/v1/checkouts/${id}`,
        {
          headers: {
            'Authorization': `Bearer ${bearerToken}`
          }
        }
      );

      return response.data.status;
    }

    async function deactivateCheckout(id) {
      const bearerToken = generateBearerToken();

      const response = await axios.post(
        `https://business.coinbase.com/api/v1/checkouts/${id}/deactivate`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${bearerToken}`
          }
        }
      );

      return response.data;
    }
    ```
  </Tab>
</Tabs>

