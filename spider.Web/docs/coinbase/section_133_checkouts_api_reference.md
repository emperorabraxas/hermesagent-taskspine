# Checkouts API Reference
Source: https://docs.cdp.coinbase.com/api-reference/business-api/rest-api/checkouts/introduction



## Introduction

The Checkouts API enables developers to create and manage checkouts for cryptocurrency payments entirely via API — no dashboard required. These APIs provide a simple way to accept payments by generating embeddable URLs that handle the payment flow, including address generation, transaction monitoring, and status updates. Real-time payment notifications are available through [webhooks](/coinbase-business/checkout-apis/webhooks).

<Note>
  To use these APIs, you need a [Coinbase Business account](https://www.coinbase.com/business).
</Note>

## Base URL

```
https://business.coinbase.com/api/v1/checkouts
```

## Authentication

All Checkouts API endpoints require authentication using a JWT Bearer token. See the [Authentication guide](/coinbase-business/authentication-authorization/api-key-authentication) for details on generating your token.

## Available Endpoints

* **[Create Checkout](/api-reference/business-api/rest-api/checkouts/create-checkout)** - Creates a new checkout
* **[List Checkouts](/api-reference/business-api/rest-api/checkouts/list-checkouts)** - Retrieves a paginated list of checkouts
* **[Get Checkout](/api-reference/business-api/rest-api/checkouts/get-checkout)** - Retrieves details of a specific checkout
* **[Deactivate Checkout](/api-reference/business-api/rest-api/checkouts/deactivate-checkout)** - Deactivates a checkout
* **[Refund Checkout](/api-reference/business-api/rest-api/checkouts/refund-checkout)** - Initiates a refund for a completed checkout

## Checkout Status

Checkouts can have the following statuses:

* `ACTIVE` - The checkout is active and can accept payments
* `PROCESSING` - The checkout is processing a payment
* `DEACTIVATED` - The checkout has been manually deactivated
* `EXPIRED` - The checkout has expired based on the `expiresAt` timestamp
* `COMPLETED` - The checkout has been successfully paid
* `FAILED` - The checkout has failed due to a payment error
* `REFUNDED` - The checkout payment has been fully refunded
* `PARTIALLY_REFUNDED` - The checkout payment has been partially refunded

## Refund Status

Refunds associated with a checkout can have the following statuses:

* `PENDING` - The refund is being processed
* `COMPLETED` - The refund has been successfully completed
* `FAILED` - The refund has failed

