# Welcome to Payment Link APIs
Source: https://docs.cdp.coinbase.com/coinbase-business/payment-link-apis/overview



<Warning>
  **The Payment Link APIs are deprecated.** Use the [Checkouts API](/coinbase-business/checkout-apis/overview) for all new integrations. If you are currently using Payment Link APIs, see the [migration guide](/coinbase-business/checkout-apis/migrate/overview).
</Warning>

## Overview

The Payment Link APIs allow you to create shareable payment URLs that handle cryptocurrency payments end-to-end. Generate links programmatically, share them with customers, and receive funds directly to your Coinbase Business account.

## Use cases

* **Crypto checkouts**: Accept crypto payments inside your app or storefront
* **E-commerce invoicing**: Send payment links with order confirmations
* **Service businesses**: Request deposits or full payments via email/SMS
* **Marketplaces**: Generate unique payment links for each transaction
* **Event ticketing**: Create time-limited payment links for reservations
* **Remote sales**: Accept payments without a website or app
* **Redirect**: Optionally redirect customers back into your app after payment completion

## Key Features

* **Simple API**: Create payment links with a single POST request
* **Real-time webhooks**: Get instant notifications when payment status changes
* **Flexible delivery**: Share via email, SMS, QR codes, or in-app

## Quick example

```bash theme={null}
curl -X POST https://business.coinbase.com/payment-links \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "50.00",
    "currency": "USD",
    "description": "Order #12345"
  }'
```

Returns a shareable payment URL ready for your customer.

## Prerequisites

Before using Payment Link APIs, you'll need:

* A [Coinbase Business account](https://www.coinbase.com/business)
* Basic understanding of REST APIs and JWT authentication

## How it works

1. **Create a link** → API returns a unique payment URL
2. **Share with customer** → Via email, SMS, or your app
3. **Customer pays** → Clicks link and sends crypto from their wallet
4. **Get notified** → Receive real-time webhook notifications
5. **Receive funds** → Auto-credited to your Coinbase Business account

## What to read next

<CardGroup>
  <Card title="Quick Start" icon="rocket" href="/coinbase-business/payment-link-apis/postman-files">
    Test the API with our Postman collection
  </Card>

  <Card title="Webhooks" icon="bell" href="/coinbase-business/payment-link-apis/webhooks">
    Set up real-time payment notifications
  </Card>

  <Card title="Authentication" icon="key" href="/coinbase-business/authentication-authorization/api-key-authentication">
    Set up API keys and JWT tokens
  </Card>

  <Card title="Integration Guide" icon="book" href="/api-reference/business-api/rest-api/payment-links/introduction">
    Step-by-step implementation guide
  </Card>
</CardGroup>

