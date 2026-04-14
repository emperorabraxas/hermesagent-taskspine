# Sandbox Environment
Source: https://docs.cdp.coinbase.com/coinbase-business/payment-link-apis/sandbox

Test your Payment Links API integration safely using the sandbox environment

## Overview

The Payment Links API sandbox environment provides a safe, isolated testing space where you can develop and test your payment link integrations without affecting production data or processing real transactions. The sandbox mirrors production functionality while using test data and simulated payment flows.

<Info>
  Authentication methods, and response formats in sandbox are identical to production, making it easy to transition your code when ready.
</Info>

## Key Differences: Sandbox vs Production

| Feature            | Sandbox                                              | Production                                   |
| ------------------ | ---------------------------------------------------- | -------------------------------------------- |
| **API Endpoint**   | `business.coinbase.com/sandbox/api/v1/payment-links` | `business.coinbase.com/api/v1/payment-links` |
| **API Keys**       | Same CDP API keys                                    | Same CDP API keys                            |
| **Transactions**   | Simulated (no real value)                            | Real payment processing                      |
| **Webhooks**       | Requires `sandbox: true` label                       | No label required                            |
| **Rate Limits**    | Same as production                                   | Standard production limits                   |
| **Data Retention** | 30 days (auto-purged)                                | Permanent                                    |

<Warning>
  **Important Limitation**: Sandbox transactions are simulated and do not involve real funds. Payments made through sandbox payment links will **not** appear in your Coinbase Business wallets. This is expected behavior for sandbox testing.

  Sandbox payments are received using **USDC on Base Sepolia testnet**. The sandbox uses an arbitrary test address (`0xC00Bb0ac72F15C3dBFc6eb58B257887b529fEF57`) for receiving payments. You can verify transactions on the [Base Sepolia Block Explorer](https://sepolia.basescan.org/address/0xC00Bb0ac72F15C3dBFc6eb58B257887b529fEF57#tokentxns).
</Warning>

## Getting Started

### 1. Prerequisites

Before using the sandbox environment, ensure you have:

* A Coinbase Business account
* CDP API credentials (same keys work for both sandbox and production)
* Familiarity with the [Payment Links API](/coinbase-business/payment-link-apis/overview)

### 2. Configure Your Application

The only change required to use sandbox is updating your API endpoint to include the `/sandbox` path segment:

<Steps>
  <Step title="Update Base URL">
    Change your API base URL to include the sandbox path:

    ```diff theme={null}
    - baseURL: 'https://business.coinbase.com/api/v1/payment-links'
    + baseURL: 'https://business.coinbase.com/sandbox/api/v1/payment-links'
    ```
  </Step>

  <Step title="Create Test Payment Links">
    Use the same API calls as production to create payment links:

    ```bash theme={null}
    cdpcurl -X POST \
      -i "YOUR_API_KEY_ID" \
      -s "YOUR_API_KEY_SECRET" \
      "https://business.coinbase.com/sandbox/api/v1/payment-links" \
      -d '{
        "amount": "10.00",
        "currency": "USDC",
        "description": "Test payment"
      }'
    ```
  </Step>

  <Step title="Test Payment Flows">
    Use the returned payment link URL to test payment flows
  </Step>
</Steps>

## Testing Payments with Testnet Funds

To fully test your sandbox integration, you'll need a wallet with testnet USDC on Base Sepolia. Here's how to set one up:

### Step 1: Get a Wallet on Base Sepolia

You can use any EVM-compatible wallet. The easiest options for non-crypto developers:

<Tabs>
  <Tab title="Coinbase Wallet (Recommended)">
    1. Download [Coinbase Wallet](https://chromewebstore.google.com/detail/coinbase-wallet-extension/hnfanknocfeofbddgcijnmhnfnkdnaad) (browser extension) or [Base](https://base.app/download) (mobile)
    2. Create a new wallet (no cryptocurrency purchase needed)
    3. In settings, enable **Developer Mode** or **Testnets**
    4. Switch network to **Base Sepolia**

    Your wallet address will look like: `0x1234...abcd`
  </Tab>

  <Tab title="MetaMask">
    1. Install [MetaMask](https://metamask.io/) browser extension
    2. Create a new wallet
    3. Add Base Sepolia network:
       * Network Name: `Base Sepolia`
       * RPC URL: `https://sepolia.base.org`
       * Chain ID: `84532`
       * Currency: `ETH`
       * Explorer: `https://sepolia.basescan.org`
    4. Switch to the Base Sepolia network
  </Tab>
</Tabs>

### Step 2: Get Testnet USDC from the Faucet

Use the Coinbase Developer Portal Faucet to claim free testnet USDC:

1. Go to the [Coinbase Developer Portal Faucet](https://portal.cdp.coinbase.com/products/faucet)
2. Sign in with your Coinbase account (the same account you use for Coinbase Business)
3. Select **Network**: Base Sepolia
4. Select **Token**: USDC
5. Enter your wallet address from Step 1
6. Click **Claim**

You'll receive 1 USDC (testnet) - enough to test multiple payment links.

<Info>
  Faucet limits: 10 USDC claims per 24 hours. See [Faucets documentation](/faucets/introduction/welcome) for full details.
</Info>

### Step 3: Test a Payment

Now you can test the full payment flow:

1. Create a sandbox payment link (see [Getting Started](#getting-started) above)
2. Open the payment link URL in your browser
3. Connect your testnet wallet when prompted
4. Approve the USDC payment
5. Verify your webhook receives the `payment_link.payment.success` event
6. Confirm the transaction on [Base Sepolia Explorer](https://sepolia.basescan.org/)

<Tip>
  **For developers without crypto experience**: You don't need to buy or hold any real cryptocurrency. Testnet tokens have no monetary value and are free to claim.
</Tip>

## API Endpoints

All Payment Links API endpoints are available in sandbox with the `/sandbox` path prefix:

| Endpoint                | Sandbox URL                                 |
| ----------------------- | ------------------------------------------- |
| Create Payment Link     | `POST /sandbox/api/v1/payment-links`        |
| List Payment Links      | `GET /sandbox/api/v1/payment-links`         |
| Get Payment Link        | `GET /sandbox/api/v1/payment-links/{id}`    |
| Deactivate Payment Link | `DELETE /sandbox/api/v1/payment-links/{id}` |

The request and response schemas are identical to production. No changes to API contracts are needed when switching between environments.

## Webhook Events

Sandbox webhook events work the same as production but are differentiated using the `sandbox` label. This allows you to:

* Test webhook integration without receiving production events
* Validate your webhook handler with realistic event payloads
* Test failure scenarios and retry logic safely

### Subscribing to Sandbox Webhooks

To receive webhook events for sandbox payment links, create a subscription with `"sandbox": "true"` in the labels:

```bash theme={null}
cdpcurl -X POST \
  -i "YOUR_API_KEY_ID" \
  -s "YOUR_API_KEY_SECRET" \
  "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
  -d '{
    "description": "Sandbox payment link webhooks",
    "eventTypes": [
      "payment_link.payment.success",
      "payment_link.payment.failed",
      "payment_link.payment.expired"
    ],
    "target": {
      "url": "https://your-webhook-url.com/sandbox",
      "method": "POST"
    },
    "labels": {
      "sandbox": "true"
    },
    "isEnabled": true
  }'
```

### Webhook Event Types

The same event types are available for both sandbox and production:

| Event Type                     | Description                          |
| ------------------------------ | ------------------------------------ |
| `payment_link.payment.success` | Payment link successfully paid       |
| `payment_link.payment.failed`  | Payment link payment failed          |
| `payment_link.payment.expired` | Payment link expired without payment |

For complete webhook setup instructions and signature verification, see the [Webhooks documentation](/coinbase-business/payment-link-apis/webhooks).

## Best Practices

<AccordionGroup>
  <Accordion title="Isolate Sandbox Configuration">
    Keep sandbox configuration completely separate from production:

    ```typescript theme={null}
    // config.ts
    const config = {
      sandbox: {
        apiUrl: 'https://business.coinbase.com/sandbox/api/v1/payment-links',
      },
      production: {
        apiUrl: 'https://business.coinbase.com/api/v1/payment-links',
      }
    };

    export const getConfig = () => {
      return process.env.NODE_ENV === 'production'
        ? config.production
        : config.sandbox;
    };
    ```
  </Accordion>

  <Accordion title="Test Error Scenarios">
    Use sandbox to thoroughly test error scenarios:

    * Invalid authentication
    * Malformed requests
    * Payment failures
    * Expired payment links
  </Accordion>

  <Accordion title="Separate Webhook Subscriptions">
    Create separate webhook subscriptions for sandbox and production:

    ```json theme={null}
    // Sandbox subscription - requires sandbox label
    {
      "labels": { "sandbox": "true" },
      "target": { "url": "https://your-app.com/webhooks/sandbox" }
    }

    // Production subscription
    {
      "labels": {},
      "target": { "url": "https://your-app.com/webhooks/production" }
    }
    ```
  </Accordion>

  <Accordion title="Automate Integration Tests">
    Create automated test suites that run against sandbox:

    ```typescript theme={null}
    describe('Payment Links API Integration', () => {
      const baseUrl = 'https://business.coinbase.com/sandbox/api/v1/payment-links';

      test('should create payment link', async () => {
        const response = await createPaymentLink({
          amount: '10.00',
          currency: 'USDC',
          description: 'Test payment'
        });

        expect(response.id).toBeDefined();
        expect(response.status).toBe('ACTIVE');
      });

      test('should list payment links', async () => {
        const response = await listPaymentLinks();
        expect(Array.isArray(response.data)).toBe(true);
      });
    });
    ```
  </Accordion>
</AccordionGroup>

## Limitations & Considerations

<Warning>
  Be aware of these sandbox limitations when testing:
</Warning>

* **Simulated Transactions**: Sandbox payments do not involve real funds
* **No Wallet Updates**: Payments will not appear in your Coinbase app wallet
* **Data Retention**: Sandbox data is automatically purged after 30 days
* **Performance**: Response times may vary from production
* **Third-Party Services**: Some third-party integrations may use mocked responses

## Transitioning to Production

When you're ready to move from sandbox to production:

<Steps>
  <Step title="Complete Integration Testing">
    Ensure all features work correctly in sandbox with comprehensive test coverage
  </Step>

  <Step title="Review Webhook Configuration">
    * Verify you have a webhook subscription for production (no sandbox label needed)
    * Ensure your production webhook endpoint is ready to receive events
  </Step>

  <Step title="Update Configuration">
    Switch from sandbox to production endpoints:

    ```diff theme={null}
    - baseURL: 'https://business.coinbase.com/sandbox/api/v1/payment-links'
    + baseURL: 'https://business.coinbase.com/api/v1/payment-links'
    ```
  </Step>

  <Step title="Test with Small Amounts">
    Begin with small payment amounts to verify everything works as expected
  </Step>

  <Step title="Monitor Closely">
    Set up monitoring and alerting for:

    * Failed payments
    * API errors
    * Webhook delivery failures
  </Step>
</Steps>

## Troubleshooting

<AccordionGroup>
  <Accordion title="401 Unauthorized Errors">
    **Problem**: Getting authentication errors in sandbox

    **Solutions**:

    * Verify your CDP API keys are valid
    * Check that the API key has the required permissions
    * Ensure the `Authorization` header is properly formatted
    * Confirm the API key hasn't expired
  </Accordion>

  <Accordion title="Not Receiving Sandbox Webhooks">
    **Problem**: Webhook events are not being delivered for sandbox payment links

    **Solutions**:

    * Verify your subscription has `"sandbox": "true"` in labels
    * Check that your webhook endpoint is accessible and returns 200 OK
    * Ensure you're subscribed to the correct event types
    * Review webhook signature verification is implemented correctly
  </Accordion>

  <Accordion title="Payment Link URL Not Working">
    **Problem**: Unable to complete payment on sandbox payment link

    **Solutions**:

    * Verify the payment link hasn't expired
    * Check the payment link status via API
    * Ensure the payment link is still active
  </Accordion>

  <Accordion title="Funds Not Appearing in Wallet">
    **Problem**: Completed sandbox payments not showing in Coinbase wallet

    **This is expected behavior**: Sandbox payments are simulated and will not appear in your Coinbase wallet. To verify payments, check the payment link status via API or webhook events.
  </Accordion>

  <Accordion title="Environment Mismatch">
    **Problem**: Code works in sandbox but fails in production (or vice versa)

    **Solutions**:

    * Verify all configuration uses environment variables
    * Check for hardcoded sandbox-specific URLs
    * Ensure webhook subscriptions have correct `sandbox` label values
  </Accordion>
</AccordionGroup>

## Additional Resources

<CardGroup>
  <Card title="API Reference" icon="book" href="/api-reference/business-api/rest-api/introduction">
    Complete API documentation for Payment Links endpoints
  </Card>

  <Card title="Webhooks Guide" icon="webhook" href="/coinbase-business/payment-link-apis/webhooks">
    Learn how to set up and verify webhook events
  </Card>

  <Card title="Authentication" icon="key" href="/get-started/authentication/overview">
    Learn how to authenticate your API requests
  </Card>

  <Card title="Postman Collection" icon="code" href="/coinbase-business/payment-link-apis/postman-files">
    Download Postman files for testing
  </Card>
</CardGroup>

