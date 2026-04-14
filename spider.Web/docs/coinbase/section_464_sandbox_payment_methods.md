# Sandbox: Payment Methods
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/sandbox/guides/payment-methods



## Overview

Payment methods represent external financial instruments (like bank accounts via Fedwire and SWIFT) that you can use to move money. They are entity-level and you can use them with any of your accounts.

**Key differences:**

* **Accounts** hold assets and balances (e.g., your USD account)
* **Payment methods** are external destinations (e.g., your JPMorgan Chase bank account)

**Example:** You have \$1000 in your Coinbase USD account. You can withdraw \$100 to your JPMorgan Chase bank, then later withdraw \$200 to your Bank of America account. Each external bank is a separate payment method.

In Sandbox, three test payment methods are automatically created at the entity level and can be used with all your accounts.

<Info>
  Currently, payment methods are only supported as targets for transfers (withdrawals from your account to a bank).
</Info>

## Pre-configured payment methods

Three test payment methods are automatically created in your Sandbox environment:

<Tip>
  Test transfer flows with both active and inactive payment methods to ensure your integration properly handles success and error states before going to production.
</Tip>

| Payment Rail | Bank                   | Status     | Behavior          |
| ------------ | ---------------------- | ---------- | ----------------- |
| Fedwire      | JPMorgan Chase Bank NA | `active`   | Transfers succeed |
| Fedwire      | Bank of America NA     | `inactive` | Transfers fail    |
| SWIFT        | Deutsche Bank          | `active`   | Transfers succeed |

## Prerequisites

Complete the [Quickstart](/api-reference/payment-apis/sandbox/quickstart) before proceeding if you do not yet have Sandbox API keys or a funded account.

Ensure you have set your API key as an environment variable:

```bash theme={null}
export CDP_API_KEY=~/Downloads/cdp_api_key.json
```

## 1. List payment methods

See your available test methods, their `paymentMethodId` values, and other details:

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  'https://sandbox.cdp.coinbase.com/platform/v2/payment-methods'
```

<Accordion title="Example response">
  ```json theme={null}
  {
    "paymentMethods": [
      {
        "paymentMethodId": "paymentMethod_398435cb-03bd-5568-b8d5-44accd7ce305",
        "active": true,
        "paymentRail": "fedwire",
        "fedwire": {
          "bankName": "JPMorgan Chase Bank NA",
          "accountLast4": "9012",
          "routingNumber": "021000021",
          "asset": "usd"
        }
      },
      {
        "paymentMethodId": "paymentMethod_82933da3-bd1e-5c8d-a05f-9ef912e5bce9",
        "active": false,
        "paymentRail": "fedwire",
        "fedwire": {
          "bankName": "Bank of America NA",
          "accountLast4": "1098",
          "routingNumber": "026009593",
          "asset": "usd"
        }
      },
      {
        "paymentMethodId": "paymentMethod_d984c884-7fef-51e8-98a2-742ba6e32515",
        "active": true,
        "paymentRail": "swift",
        "swift": {
          "bankName": "Deutsche Bank",
          "bic": "DEUTDEFF",
          "ibanLast4": "3000",
          "asset": "usd"
        }
      }
    ]
  }
  ```
</Accordion>

## 2. Test transfer flows

Use payment methods as targets to test transfer flows.

<Tip>
  You will need your `accountId` and `paymentMethodId` values in the next step:

  ```bash theme={null}
  cdpcurl -k $CDP_API_KEY 'https://sandbox.cdp.coinbase.com/platform/v2/payment-methods' | sed '1d' | jq -r '.paymentMethods[].paymentMethodId'; cdpcurl -k $CDP_API_KEY 'https://sandbox.cdp.coinbase.com/platform/v2/accounts' | sed '1d' | jq -r '.accounts[].accountId'
  ```
</Tip>

Set your IDs as environment variables:

```bash theme={null}
export ACCOUNT_ID="account_abc123..."           # Your account ID
export ACTIVE_PM_ID="paymentMethod_xyz789..."   # Active payment method ID
export INACTIVE_PM_ID="paymentMethod_def456..." # Inactive payment method ID
```

<Note>
  The escaped quotes (`\"`) in the following commands are required for bash variable substitution in JSON.
</Note>

### Successful transfer

This simulates transferring from your Sandbox account to an **active payment method**:

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  -X POST \
  -d "{
    \"source\": {
      \"accountId\": \"$ACCOUNT_ID\",
      \"asset\": \"usd\"
    },
    \"target\": {
      \"paymentMethodId\": \"$ACTIVE_PM_ID\",
      \"asset\": \"usd\"
    },
    \"amount\": \"5.00\",
    \"asset\": \"usd\",
    \"execute\": true
  }" \
  'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
```

The transfer completes successfully, your account balance decreases, and you receive webhook events (`payment.transfer.processing` → `payment.transfer.completed`).

<Accordion title="Example response">
  ```json theme={null}
  {
    "transferId": "transfer_8b707d29-4690-4948-b645-de1cd1f5fd05",
    "status": "completed",
    "source": {
      "accountId": "account_db458f63-418a-4a91-a045-fab93ac35c3f",
      "asset": "usd"
    },
    "target": {
      "paymentMethodId": "paymentMethod_398435cb-03bd-5568-b8d5-44accd7ce305",
      "asset": "usd"
    },
    "sourceAmount": "5",
    "sourceAsset": "usd",
    "targetAmount": "5",
    "targetAsset": "usd",
    "createdAt": "2026-02-11T23:19:24.086Z",
    "updatedAt": "2026-02-11T23:19:24.183Z"
  }
  ```
</Accordion>

### Failed transfer

This simulates transferring to an **inactive payment method** to test error handling:

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  -X POST \
  -d "{
    \"source\": {
      \"accountId\": \"$ACCOUNT_ID\",
      \"asset\": \"usd\"
    },
    \"target\": {
      \"paymentMethodId\": \"$INACTIVE_PM_ID\",
      \"asset\": \"usd\"
    },
    \"amount\": \"5.00\",
    \"asset\": \"usd\",
    \"execute\": true
  }" \
  'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
```

The transfer fails with an error response. Use this to test how your application handles failed transfers.

<Accordion title="Example error response">
  ```json theme={null}
  {
    "errorType": "invalid_request",
    "errorMessage": "Target payment method payment method id is invalid.",
    "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid-request",
    "correlationId": "9cc7d1cd1cae8b7e-IAD"
  }
  ```
</Accordion>

For more transfer examples, see the [Transfers guide](/api-reference/payment-apis/sandbox/guides/transfers).

## API reference

* [List Payment Methods](/api-reference/payment-apis/rest-api/payment-methods-under-development/list-payment-methods)
* [Create a Transfer](/api-reference/payment-apis/rest-api/transfers-under-development/create-a-transfer)

