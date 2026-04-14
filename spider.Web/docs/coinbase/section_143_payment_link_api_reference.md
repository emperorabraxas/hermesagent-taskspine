# Payment Link API Reference
Source: https://docs.cdp.coinbase.com/api-reference/business-api/rest-api/payment-links/introduction



<Warning>
  **The Payment Link API is deprecated.** Use the [Checkouts API](/api-reference/business-api/rest-api/checkouts/introduction) for all new integrations. If you are currently using the Payment Link API, see the [migration guide](/coinbase-business/checkout-apis/migrate/overview).
</Warning>

## Introduction

The Payment Link API enables developers to create and manage payment links for cryptocurrency payments. These APIs provide a simple way to request payments from users by generating shareable URLs that handle the payment flow, including address generation, transaction monitoring, and status updates. Real-time payment notifications are available through [webhooks](/coinbase-business/payment-link-apis/webhooks).

<Note>
  To use these APIs, you need a [Coinbase Business account](https://www.coinbase.com/business).
</Note>

## Base URL

```
https://business.coinbase.com/api/v1/payment-links
```

## Authentication

All Payment Link API endpoints require authentication using a JWT Bearer token. See the [Authentication guide](/coinbase-business/authentication-authorization/api-key-authentication) for details on generating your token.

## Available Endpoints

* **[Create Payment Link](/api-reference/business-api/rest-api/payment-links/create-payment-link)** - Creates a new payment link
* **[List Payment Links](/api-reference/business-api/rest-api/payment-links/list-payment-links)** - Retrieves a paginated list of payment links
* **[Get Payment Link](/api-reference/business-api/rest-api/payment-links/get-payment-link)** - Retrieves details of a specific payment link
* **[Deactivate Payment Link](/api-reference/business-api/rest-api/payment-links/deactivate-payment-link)** - Deactivates a payment link

## Payment Link Status

Payment links can have the following statuses:

* `ACTIVE` - The payment link is active and can accept payments
* `DEACTIVATED` - The payment link has been manually deactivated
* `EXPIRED` - The payment link has expired based on the `expiresAt` timestamp
* `COMPLETED` - The payment link has been successfully paid

