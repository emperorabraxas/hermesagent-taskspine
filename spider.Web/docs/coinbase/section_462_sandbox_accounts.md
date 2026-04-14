# Sandbox: Accounts
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/sandbox/guides/accounts

List and view account details via API

## Overview

Accounts are containers that hold assets and can be used for transacting. In Sandbox, create accounts through the Portal UI.

<Info>
  Sandbox accounts are isolated from production and do not require linking to any external Coinbase accounts.
</Info>

## Prerequisites

Before you begin, you need `cdpcurl` and a Sandbox API key. See the [Quickstart](/api-reference/payment-apis/sandbox/quickstart) for instructions.

## 1. List accounts

See all your Sandbox accounts:

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  'https://sandbox.cdp.coinbase.com/platform/v2/accounts'
```

<Accordion title="Example response">
  ```json theme={null}
  {
    "accounts": [
      {
        "accountId": "account_db458f63-418a-4a91-a045-fab93ac35c3f",
        "name": "My Test Account",
        "createdAt": "2026-02-11T20:00:00Z",
        "updatedAt": "2026-02-11T20:00:00Z"
      }
    ]
  }
  ```
</Accordion>

<Tip>
  To get just your account IDs:

  ```bash theme={null}
  cdpcurl -k $CDP_API_KEY \
    'https://sandbox.cdp.coinbase.com/platform/v2/accounts' | sed '1d' | jq -r '.accounts[].accountId'
  ```
</Tip>

## 2. Get account details

View detailed account information including balances:

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  'https://sandbox.cdp.coinbase.com/platform/v2/accounts/YOUR_ACCOUNT_ID'
```

<Accordion title="Example response">
  ```json theme={null}
  {
    "accountId": "account_db458f63-418a-4a91-a045-fab93ac35c3f",
    "name": "My Test Account",
    "balances": [
      {
        "asset": "usd",
        "amount": "1000.00"
      },
      {
        "asset": "usdc",
        "amount": "500.00"
      }
    ],
    "createdAt": "2026-02-11T20:00:00Z",
    "updatedAt": "2026-02-11T23:00:00Z"
  }
  ```
</Accordion>

## Using Portal UI

You can create, manage, and fund accounts through the Portal UI:

<Steps>
  <Step title="Access your account">
    Navigate to [Portal Accounts](https://portal.cdp.coinbase.com/v2/sandbox) in Sandbox
  </Step>

  <Step title="Create account">
    Name the account (e.g., "My Test Account")
  </Step>

  <Step title="Edit test assets">
    Add a balance to your account. Currently we support USD, USDC, USDT (e.g., set USD to \$1000)
  </Step>
</Steps>

<Frame>
  <img alt="Sandbox account showing test balances for USD, USDT, and USDC" />
</Frame>

<Note>
  Account funding is **only available** through the Portal UI. All balances are simulated within the Sandbox environment.
</Note>

## What to read next

<CardGroup>
  <Card title="List Accounts" icon="list" href="/api-reference/payment-apis/rest-api/accounts-under-development/list-accounts">
    API reference for listing accounts
  </Card>

  <Card title="Get Account" icon="wallet" href="/api-reference/payment-apis/rest-api/accounts-under-development/get-an-account">
    API reference for getting account details
  </Card>
</CardGroup>

