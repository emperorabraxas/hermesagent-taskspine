# Sandbox: Transfers
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/sandbox/guides/transfers

Test transfers to crypto addresses and emails in Sandbox

## Overview

Transfers move funds to external addresses, other Coinbase users, or payment methods. In Sandbox, all transfers are simulated—webhooks fire and status transitions occur, but no real transactions happen.

## Prerequisites

Before you begin, you need `cdpcurl`, a Sandbox API key, and a funded account. See the [Quickstart](/api-reference/payment-apis/sandbox/quickstart) for instructions.

## 1. Simulate transfer by target type

Set your account ID:

```bash theme={null}
export ACCOUNT_ID="account_db458f63-..."
```

<Accordion title="Get your account ID">
  ```bash theme={null}
  cdpcurl -k $CDP_API_KEY \
    'https://sandbox.cdp.coinbase.com/platform/v2/accounts' | sed '1d' | jq -r '.accounts[].accountId'
  ```
</Accordion>

### a. To reserved addresses

<Info>
  You can use any valid address format for the network—it doesn't need to be a real or funded address. Use reserved addresses below to test specific error scenarios.
</Info>

Use these reserved addresses to test specific success and failure scenarios:

<Warning>
  Any funds sent **in production** to these addresses will be lost. In Sandbox, they are simulated and used for **testing purposes** only.
</Warning>

| Reserved Address                             | Simulated Outcome       |
| -------------------------------------------- | ----------------------- |
| `0x1111111111111111111111111111111111111111` | Success                 |
| `0x2222222222222222222222222222222222222222` | Transfer invalid target |
| `0x3333333333333333333333333333333333333333` | Invalid address         |
| `0x4444444444444444444444444444444444444444` | Unsupported network     |

<Tabs>
  <Tab title="Success">
    Below is a simulation using `0x1111...` to test successful transfer handling:

    ```bash theme={null}
    cdpcurl -k $CDP_API_KEY \
      -X POST \
      -d "{
        \"source\": {
          \"accountId\": \"$ACCOUNT_ID\",
          \"asset\": \"usdc\"
        },
        \"target\": {
          \"network\": \"base\",
          \"address\": \"0x1111111111111111111111111111111111111111\",
          \"asset\": \"usdc\"
        },
        \"amount\": \"5.00\",
        \"asset\": \"usdc\",
        \"execute\": true
      }" \
      'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
    ```

    Expected response: HTTP `2xx` with normal transfer response
  </Tab>

  <Tab title="Transfer invalid target">
    Below is a simulation using `0x2222...` to test malformed target error handling:

    ```bash theme={null}
    cdpcurl -k $CDP_API_KEY \
      -X POST \
      -d "{
        \"source\": {
          \"accountId\": \"$ACCOUNT_ID\",
          \"asset\": \"usdc\"
        },
        \"target\": {
          \"network\": \"base\",
          \"address\": \"0x2222222222222222222222222222222222222222\",
          \"asset\": \"usdc\"
        },
        \"amount\": \"5.00\",
        \"asset\": \"usdc\",
        \"execute\": true
      }" \
      'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
    ```

    Expected response: HTTP `400`

    ```json theme={null}
    {
      "errorType": "invalid_request",
      "errorMessage": "'target' is invalid: must match one of [Account, Payment Method, Onchain Address, Email Instrument]. Account requires 'accountId'; Payment Method requires 'paymentMethodId'; Onchain Address requires 'network'; Email Instrument requires 'email'"
    }
    ```
  </Tab>

  <Tab title="Invalid address">
    Below is a simulation using `0x3333...` to test invalid address error handling:

    ```bash theme={null}
    cdpcurl -k $CDP_API_KEY \
      -X POST \
      -d "{
        \"source\": {
          \"accountId\": \"$ACCOUNT_ID\",
          \"asset\": \"usdc\"
        },
        \"target\": {
          \"network\": \"base\",
          \"address\": \"0x3333333333333333333333333333333333333333\",
          \"asset\": \"usdc\"
        },
        \"amount\": \"5.00\",
        \"asset\": \"usdc\",
        \"execute\": true
      }" \
      'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
    ```

    Expected response: HTTP `400`

    ```json theme={null}
    {
      "errorType": "invalid_request",
      "errorMessage": "Invalid onchain address for network base."
    }
    ```
  </Tab>

  <Tab title="Unsupported network">
    Below is a simulation using `0x4444...` to test invalid network parameter handling:

    ```bash theme={null}
    cdpcurl -k $CDP_API_KEY \
      -X POST \
      -d "{
        \"source\": {
          \"accountId\": \"$ACCOUNT_ID\",
          \"asset\": \"usdc\"
        },
        \"target\": {
          \"network\": \"base\",
          \"address\": \"0x4444444444444444444444444444444444444444\",
          \"asset\": \"usdc\"
        },
        \"amount\": \"5.00\",
        \"asset\": \"usdc\",
        \"execute\": true
      }" \
      'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
    ```

    Expected response: HTTP `400`

    ```json theme={null}
    {
      "errorType": "invalid_request",
      "errorMessage": "base is not a supported network."
    }
    ```
  </Tab>
</Tabs>

<Info>
  The target address can be any valid format for the network—it doesn't need to be a real or funded address. Use reserved addresses to test specific scenarios.
</Info>

### b. To reserved email addresses

Send to a Coinbase user by email. In Sandbox, only whitelisted test emails work:

| Test Email             | Description                   |
| ---------------------- | ----------------------------- |
| `testuser1@domain.com` | Returns successful validation |
| `testuser2@domain.com` | Returns successful validation |

You can also use the following reserved email address to simulate a deterministic error response:

| Reserved Email                    | Simulated Outcome    |
| --------------------------------- | -------------------- |
| `sandboxinvalidtarget@domain.com` | Invalid email target |

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  -X POST \
  -d "{
    \"source\": {
      \"accountId\": \"$ACCOUNT_ID\",
      \"asset\": \"usdc\"
    },
    \"target\": {
      \"email\": \"sandboxinvalidtarget@domain.com\",
      \"asset\": \"usdc\"
    },
    \"amount\": \"10\",
    \"asset\": \"usdc\",
    \"execute\": true
  }" \
  'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
```

Expected response: HTTP `400`

```json theme={null}
{
    "correlationId": "90d67ad3-d067-41d8-816f-10f3a0144502",
    "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid-request",
    "errorMessage": "Target email is invalid.",
    "errorType": "invalid_request"
}
```

<Accordion title="Get your account ID">
  ```bash theme={null}
  cdpcurl -k $CDP_API_KEY \
    'https://sandbox.cdp.coinbase.com/platform/v2/accounts' | sed '1d' | jq -r '.accounts[].accountId'
  ```
</Accordion>

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  -X POST \
  -d "{
    \"source\": {
      \"accountId\": \"$ACCOUNT_ID\",
      \"asset\": \"usd\"
    },
    \"target\": {
      \"email\": \"testuser1@domain.com\",
      \"asset\": \"usd\"
    },
    \"amount\": \"5.00\",
    \"asset\": \"usd\",
    \"execute\": true
  }" \
  'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
```

<Warning>
  Any email **not** in the whitelist returns a `4xx` error. This prevents privacy concerns around validating real email addresses in Sandbox.
</Warning>

### c. To reserved payment methods

For testing fiat withdrawals to external banks (Fedwire, SWIFT), see the [Payment Methods guide](/api-reference/payment-apis/sandbox/guides/payment-methods).

Payment methods have pre-built test scenarios for different use cases (e.g., active vs inactive methods).

## 2. Validate before executing

Use `validateOnly: true` to verify recipient details (like email addresses or crypto addresses) before executing a transfer.

<Accordion title="Get your account ID">
  ```bash theme={null}
  cdpcurl -k $CDP_API_KEY \
    'https://sandbox.cdp.coinbase.com/platform/v2/accounts' | sed '1d' | jq -r '.accounts[].accountId'
  ```
</Accordion>

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  -X POST \
  -d "{
    \"source\": {
      \"accountId\": \"$ACCOUNT_ID\",
      \"asset\": \"usd\"
    },
    \"target\": {
      \"email\": \"testuser1@domain.com\",
      \"asset\": \"usd\"
    },
    \"amount\": \"5.00\",
    \"asset\": \"usd\",
    \"validateOnly\": true
  }" \
  'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
```

A `2xx` response means the transfer would succeed. A `4xx` response includes an `errorType` explaining why validation failed.

<Tip>
  Use the [reserved addresses from section 1.a](#a-to-reserved-addresses) to test validation scenarios for crypto addresses (e.g., validate with `0x3333...` to test invalid address handling).
</Tip>

## 3. List transfers

View all transfers for your account:

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  'https://sandbox.cdp.coinbase.com/platform/v2/transfers'
```

<Accordion title="Example response">
  ```json theme={null}
  {
    "transfers": [
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
    ]
  }
  ```
</Accordion>

## What to read next

<CardGroup>
  <Card title="Create Transfer" icon="arrow-right" href="/api-reference/payment-apis/rest-api/transfers-under-development/create-a-transfer">
    API reference for creating transfers
  </Card>

  <Card title="List Transfers" icon="list" href="/api-reference/payment-apis/rest-api/transfers-under-development/list-transfers">
    API reference for listing transfers
  </Card>
</CardGroup>

