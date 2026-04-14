# Migrate from Payment Links Overview
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/migrate/overview



## Overview

Migrate from the Payment Link API to the Checkouts API for improved reliability and a modernized response schema. This guide covers the key changes and provides code examples to help you update your integration.

<Accordion title="Migration summary">
  <Steps>
    <Step title="Update base URL">
      From `api/v1/payment-links` to `api/v1/checkouts`
    </Step>

    <Step title="Update request/response handling">
      New field names and response schema
    </Step>

    <Step title="Update webhook event types">
      From `payment_link.*` to `checkout.*` events
    </Step>

    <Step title="Update ID references">
      Same 24-character hexadecimal format, new resource type
    </Step>

    <Step title="Test thoroughly">
      Verify status values, webhook payloads, and redirect flows
    </Step>
  </Steps>
</Accordion>

## Key differences

| Component             | Payment Link API                                     | Checkouts API                                    |
| :-------------------- | :--------------------------------------------------- | :----------------------------------------------- |
| **Base URL**          | `https://business.coinbase.com/api/v1/payment-links` | `https://business.coinbase.com/api/v1/checkouts` |
| **Resource name**     | Payment Link                                         | Checkout                                         |
| **Path parameter**    | `paymentLinkId`                                      | `id`                                             |
| **List response key** | `paymentLinks`                                       | `checkouts`                                      |

### Webhook event mapping

| Payment Link API Event         | Checkouts API Event        |
| :----------------------------- | :------------------------- |
| `payment_link.payment.success` | `checkout.payment.success` |
| `payment_link.payment.failed`  | `checkout.payment.failed`  |
| `payment_link.payment.expired` | `checkout.payment.expired` |

## Migration checklist

### 1. Update API integration

* Update base URL to `https://business.coinbase.com/api/v1/checkouts`
* Update path parameter from `paymentLinkId` to `id`
* Update list response parsing from `paymentLinks` to `checkouts`

### 2. Update webhook subscriptions

* Create new webhook subscriptions with `checkout.*` event types
* Keep existing `payment_link.*` subscriptions until migration is complete
* Delete old subscriptions once fully migrated

### 3. Update status handling

* Status values are identical (`ACTIVE`, `PROCESSING`, `DEACTIVATED`, `EXPIRED`, `COMPLETED`, `FAILED`)
* No changes to fulfillment logic for status transitions

### 4. Test and validate

* Test in the [sandbox environment](/coinbase-business/checkout-apis/sandbox)
* Verify all webhook event types are handled correctly
* Verify redirect URLs still function correctly

### 5. Monitor and observe

* Keep both subscriptions running in parallel during transition
* Monitor for any missed events
* Cut over fully once confident in new integration

## What to read next

* [API & Schema Mapping](/coinbase-business/checkout-apis/migrate/api-schema-mapping) - Detailed endpoint and response comparisons with code examples
* [FAQ](/coinbase-business/checkout-apis/migrate/faq) - Common questions and troubleshooting

