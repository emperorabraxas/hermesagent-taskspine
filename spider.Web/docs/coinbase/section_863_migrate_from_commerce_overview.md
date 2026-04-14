# Migrate from Commerce Overview
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/migrate-from-commerce/overview



## Overview

Migrate from Commerce Charge API to the Checkouts API for improved reliability, simplified integration, modern authentication, and additional capabilities including settlement details. This guide covers the key changes and provides code examples to help you update your integration.

<Note>
  Checkouts API requires a [Coinbase Business account](https://www.coinbase.com/business).
</Note>

<Accordion title="Migration summary">
  <Steps>
    <Step title="Update authentication">
      Switch from API key to JWT Bearer tokens
    </Step>

    <Step title="Change base URL">
      From `api.commerce.coinbase.com` to `business.coinbase.com/api/v1/checkouts`
    </Step>

    <Step title="Update request/response handling">
      New field names and flattened structure
    </Step>

    <Step title="Implement status monitoring">
      Use webhooks for real-time notifications or polling
    </Step>

    <Step title="Test thoroughly">
      New ID formats and status values require updates to your logic
    </Step>
  </Steps>
</Accordion>

## Key differences

| Component              | Charge API (Commerce)               | Checkouts API                          |
| :--------------------- | :---------------------------------- | :------------------------------------- |
| **Base URL**           | `https://api.commerce.coinbase.com` | `https://business.coinbase.com/api/v1` |
| **Authentication**     | `X-CC-Api-Key` header               | Bearer token with CDP API key          |
| **Primary resource**   | Charge                              | Checkout                               |
| **ID format**          | UUID                                | 24-character hexadecimal               |
| **Payment URL field**  | `hosted_url`                        | `url`                                  |
| **Settlement details** | Not available                       | `settlement` object with fee breakdown |

<Info>
  Checkouts API requires [CDP API key authentication](/coinbase-business/authentication-authorization/api-key-authentication).
</Info>

### Status and field mappings

| Feature                   | Charge API                                       | Checkouts API                                               |
| :------------------------ | :----------------------------------------------- | :---------------------------------------------------------- |
| **Status values**         | NEW, SIGNED, PENDING, COMPLETED, EXPIRED, FAILED | ACTIVE, PROCESSING, COMPLETED, DEACTIVATED, EXPIRED, FAILED |
| **Amount structure**      | `local_price.amount` and `local_price.currency`  | `amount` and `currency` (flat structure)                    |
| **Network specification** | Auto-selected                                    | Explicit `network` field                                    |
| **Redirect URLs**         | `redirect_url`, `cancel_url`                     | `successRedirectUrl`, `failRedirectUrl`                     |

## Migration checklist

### 1. Update authentication

* Create CDP API keys
* Implement JWT Bearer token generation
* Update API key storage and rotation procedures
* Test authentication with Checkouts API

### 2. Update API integration

* Update base URL to `https://business.coinbase.com/api/v1/checkouts`
* Modify request bodies to match new schema
* Update response parsing to handle new fields (`address`, `settlement`, `transactionHash`)
* Implement idempotency key generation for create requests

### 3. Handle status changes

* Map Charge statuses to Checkout statuses in your system
* Update order fulfillment logic for new status values
* Set up webhooks for real-time payment notifications (see [Webhooks documentation](/coinbase-business/checkout-apis/webhooks))
* Update customer-facing status messages

### 4. Update payment flows

* Use `url` field instead of `hosted_url` for payment pages
* Update redirect URL parameters
* Test full payment flow end-to-end
* Verify metadata is correctly passed through

### 5. Handle pagination

* Update list operations to use `pageSize` and `pageToken`
* Implement `nextPageToken` handling for multiple pages
* Test pagination with large datasets

### 6. Test and validate

* Consider testing your integration with the [sandbox environment](/coinbase-business/checkout-apis/sandbox)
* Verify amount calculations (ensure proper decimal handling)
* Test expired checkout scenarios
* Test deactivation flow
* Verify metadata preservation
* Test redirect URLs

### 7. Monitor and observe

* Set up monitoring for API errors
* Track payment success rates
* Monitor checkout expiration rates
* Set up alerts for failed payments

## What to read next

* [API & Schema Mapping](/coinbase-business/checkout-apis/migrate-from-commerce/api-schema-mapping) - Detailed endpoint and response comparisons with code examples
* [FAQ](/coinbase-business/checkout-apis/migrate-from-commerce/faq) - Common questions and troubleshooting

