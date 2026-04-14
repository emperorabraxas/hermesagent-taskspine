# Deposit Destinations
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/deposit-destinations-under-development/overview



## Overview

**Deposit Destinations** allow you to manage where funds can be deposited into your accounts.

## Crypto destinations

Crypto deposit destinations are cryptocurrency addresses that you can generate via the API. Once created, these addresses can receive cryptocurrency payments on their specified network and will settle in your account balance.

**Key Features:**

* Generate unique crypto addresses for each account
* Attach metadata to track the purpose or source of deposits

**Supported Networks:**

The networks available for deposit destinations depend on your customer type ([Coinbase Business](/coinbase-business/introduction/welcome) vs [Coinbase Prime](/prime/introduction/welcome)).

See the [API and Network Support](/api-reference/payment-apis/supported-networks-assets) page for the complete list of networks and assets available for each customer type.

## Examples

**Customer Deposits:** Generate a unique deposit address for each customer to track their deposits separately:

```json theme={null}
{
  "accountId": "account_456",
  "type": "crypto",
  "network": "base",
  "metadata": {
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "reference": "789"
  }
}
```

**Invoice Payments:** Create deposit addresses tied to specific invoices:

```json theme={null}
{
  "accountId": "account_456",
  "type": "crypto",
  "network": "ethereum",
  "metadata": {
    "invoice_id": "12345",
    "order_id": "67890"
  }
}
```

## Metadata

You can attach metadata to any crypto deposit destination you create to track the purpose or source of deposits. This metadata helps you identify and reconcile incoming payments in your system.

<Warning>
  **Temporary Restriction:** Metadata values must currently be in UUID format or integer string format. Free-form metadata values will be supported in a future release.
</Warning>

**Example:**

```json theme={null}
{
  "depositDestinationId": "depositDestination_123",
  "accountId": "account_456",
  "type": "crypto",
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "network": "base",
  "metadata": {
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "order_id": "12345",
    "invoice_number": "98765"
  }
}
```

## Filtering and listing

Use the list endpoint to retrieve all deposit destinations. You can filter by **Account ID** to see deposit destinations for a specific account.

**Example:**

```bash theme={null}
GET /v2/deposit-destinations?accountId=account_123
```

## Unsupported assets

<Warning>
  **Only send supported assets to your deposit destinations.** Sending unsupported assets or using unsupported networks may result in loss of funds.

  If you accidentally send unsupported crypto, you may be able to recover it using Coinbase's [asset recovery service](https://help.coinbase.com/en/coinbase/trading-and-funding/sending-or-receiving-cryptocurrency/recover-unsupported-crypto).
</Warning>

## What to read next

* [Create a Deposit Destination](#) - Generate a new crypto deposit address
* [List Deposit Destinations](#) - View all your deposit destinations

