# Payment Acceptance API
Source: https://docs.cdp.coinbase.com/api-reference/payment-acceptance/overview



Coinbase Payment Acceptance is a full-stack stablecoin payments platform enabling instant, low-fee USDC commerce via familiar APIs, without blockchain complexity.

The Payment Acceptance API supports authorization and capture flows, instant settlement, refunds, and programmable rewards.

## Base URL

```
https://payments.coinbase.com
```

## Authentication

All API requests require authentication using a Bearer token and can be generated from your CDP API Key.

### Using your API key

Include your Bearer token in the Authorization header of each request:

```bash theme={null}
Authorization: Bearer YOUR_BEARER_TOKEN
```

### Getting started

1. [Create a CDP API Key](/get-started/authentication/cdp-api-keys) in the Coinbase Developer Platform
2. Generate a Bearer token from your API key credentials
3. Include the token in all API requests

Learn more about [CDP authentication](/get-started/authentication/cdp-api-keys).

## API Resources

<CardGroup>
  <Card title="Payments" icon="credit-card" href="/api-reference/payment-acceptance/payments/overview">
    Create payments and manage authorization, capture, charge, and void operations
  </Card>

  <Card title="Operators" icon="user" href="/api-reference/payment-acceptance/operators/create-operator">
    Create operators for payment processing
  </Card>

  <Card title="Campaigns" icon="megaphone" href="/api-reference/payment-acceptance/campaigns/create-campaign">
    Deploy onchain reward campaigns
  </Card>

  <Card title="Rewards" icon="gift" href="/api-reference/payment-acceptance/rewards/allocate-rewards">
    Allocate, distribute, deallocate, and send rewards
  </Card>

  <Card title="Webhooks" icon="webhook" href="/api-reference/payment-acceptance/webhooks/create-webhook">
    Configure endpoints for payment and reward notifications
  </Card>

  <Card title="Webhook Events" icon="bell" href="/api-reference/payment-acceptance/webhook-events/list-webhook-events">
    Query webhook events by operation or event ID
  </Card>

  <Card title="Webhook Deliveries" icon="truck" href="/api-reference/payment-acceptance/webhook-deliveries/get-webhook-deliveries-by-event-id">
    Monitor webhook delivery attempts and status
  </Card>
</CardGroup>

## OpenAPI Spec

<Card title="Download OpenAPI Spec" icon="download" href="https://docs.cdp.coinbase.com/api-reference/payment-acceptance/payment-acceptance-api.yaml">
  To use with Postman or to generate client SDKs.
</Card>

