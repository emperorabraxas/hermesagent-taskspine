# Welcome to Checkout APIs
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/overview



## Overview

The Checkout APIs allow you to create and manage embeddable checkout URLs entirely via API — no dashboard required. Generate checkouts programmatically, embed them in your app or storefront, and receive funds directly to your Coinbase Business account.

Each checkout is **single-use** — it accepts one payment and then moves to a terminal state. Create a new checkout for each transaction. You can also issue full or partial refunds for completed checkouts.

## Use cases

* **Crypto checkouts**: Accept crypto payments inside your app or storefront
* **E-commerce invoicing**: Send checkout links with order confirmations
* **Service businesses**: Request deposits or full payments via email/SMS
* **Marketplaces**: Generate unique checkout links for each transaction
* **Event ticketing**: Create time-limited checkouts for reservations
* **Remote sales**: Accept payments without a website or app
* **Redirect**: Optionally redirect customers back into your app after payment completion
* **Refunds**: Issue full or partial refunds via API with fiat currency support

## Key Features

* **Simple API**: Create checkouts with a single POST request
* **Real-time webhooks**: Get instant notifications when payment status changes
* **Flexible embedding**: Embed in your app, website, or storefront

## Quick example

```bash theme={null}
curl -X POST https://business.coinbase.com/api/v1/checkouts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "50.00",
    "currency": "USDC",
    "description": "Order #12345"
  }'
```

Returns a checkout URL ready to embed in your app or storefront.

## Prerequisites

Before using Checkout APIs, you'll need:

* A [Coinbase Business account](https://www.coinbase.com/business)
* Basic understanding of REST APIs and JWT authentication

## How it works

1. **Create a checkout** → API returns a unique checkout URL and ID
2. **Store the checkout ID** → Persist the `id` in your system to reference the checkout later
3. **Embed in your app** → Display the checkout URL in your app or storefront
4. **Customer pays** → Clicks link and sends crypto from their wallet
5. **Get notified** → Receive real-time webhook notifications
6. **Receive funds** → Auto-credited to your Coinbase Business account
7. **Refund if needed** → Issue full or partial refunds for completed checkouts via the [Refund Checkout](/api-reference/business-api/rest-api/checkouts/refund-checkout) endpoint

## What to read next

<CardGroup>
  <Card title="Webhooks" icon="bell" href="/coinbase-business/checkout-apis/webhooks">
    Set up real-time payment notifications
  </Card>

  <Card title="Authentication" icon="key" href="/coinbase-business/authentication-authorization/api-key-authentication">
    Set up API keys and JWT tokens
  </Card>

  <Card title="API Reference" icon="code" href="/api-reference/business-api/rest-api/checkouts/introduction">
    Full API endpoint documentation
  </Card>
</CardGroup>

