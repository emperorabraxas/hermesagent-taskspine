# Available APIs
Source: https://docs.cdp.coinbase.com/coinbase-app/oauth2-integration/available-apis



## Overview

You can access these APIs after a user authorizes your app via OAuth2. Each endpoint requires specific [OAuth2 scopes](/coinbase-app/oauth2-integration/scopes).

**Base URL:** `https://api.coinbase.com`

**Authentication:** Include the OAuth2 access token in the Authorization header:

```bash theme={null}
curl https://api.coinbase.com/v2/<endpoint> \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Accounts and users

| Endpoint                       | Description                                                                            | Scope                  |
| :----------------------------- | :------------------------------------------------------------------------------------- | :--------------------- |
| `GET /v2/user`                 | [Get current user's public information](/coinbase-app/track-apis/accounts)             | `wallet:user:read`     |
| `GET /v2/accounts`             | [List all user accounts and balances](/coinbase-app/track-apis/accounts#list-accounts) | `wallet:accounts:read` |
| `GET /v2/accounts/:account_id` | [Get a specific account](/coinbase-app/track-apis/accounts#show-account)               | `wallet:accounts:read` |

## Transactions

| Endpoint                                        | Description                                                                          | Scope                      |
| :---------------------------------------------- | :----------------------------------------------------------------------------------- | :------------------------- |
| `GET /v2/accounts/:account_id/transactions`     | [List transactions](/coinbase-app/track-apis/transactions#list-transactions)         | `wallet:transactions:read` |
| `GET /v2/accounts/:account_id/transactions/:id` | [Get a specific transaction](/coinbase-app/track-apis/transactions#show-transaction) | `wallet:transactions:read` |
| `POST /v2/accounts/:account_id/transactions`    | [Send crypto (requires 2FA)](/coinbase-app/transfer-apis/send-crypto)                | `wallet:transactions:send` |

## Addresses

| Endpoint                                  | Description                                                           | Scope                     |
| :---------------------------------------- | :-------------------------------------------------------------------- | :------------------------ |
| `GET /v2/accounts/:account_id/addresses`  | [List addresses](/coinbase-app/transfer-apis/onchain-addresses)       | `wallet:addresses:read`   |
| `POST /v2/accounts/:account_id/addresses` | [Create a new address](/coinbase-app/transfer-apis/onchain-addresses) | `wallet:addresses:create` |

## Deposits & withdrawals

| Endpoint                                                          | Description                                                                      | Scope                       |
| :---------------------------------------------------------------- | :------------------------------------------------------------------------------- | :-------------------------- |
| `GET /v2/accounts/:account_id/deposits`                           | [List deposits](/coinbase-app/transfer-apis/deposit-fiat#list-deposits)          | `wallet:deposits:read`      |
| `GET /v2/accounts/:account_id/deposits/:deposit_id`               | [Show deposit](/coinbase-app/transfer-apis/deposit-fiat#show-deposit)            | `wallet:deposits:read`      |
| `POST /v2/accounts/:account_id/deposits`                          | [Deposit fiat funds](/coinbase-app/transfer-apis/deposit-fiat#deposit-funds)     | `wallet:deposits:create`    |
| `POST /v2/accounts/:account_id/deposits/:deposit_id/commit`       | [Commit deposit](/coinbase-app/transfer-apis/deposit-fiat#commit-deposit)        | `wallet:deposits:create`    |
| `GET /v2/accounts/:account_id/withdrawals`                        | [List withdrawals](/coinbase-app/transfer-apis/withdraw-fiat#list-withdrawals)   | `wallet:withdrawals:read`   |
| `GET /v2/accounts/:account_id/withdrawals/:withdrawal_id`         | [Show withdrawal](/coinbase-app/transfer-apis/withdraw-fiat#show-withdrawal)     | `wallet:withdrawals:read`   |
| `POST /v2/accounts/:account_id/withdrawals`                       | [Withdraw fiat funds](/coinbase-app/transfer-apis/withdraw-fiat#withdraw-funds)  | `wallet:withdrawals:create` |
| `POST /v2/accounts/:account_id/withdrawals/:withdrawal_id/commit` | [Commit withdrawal](/coinbase-app/transfer-apis/withdraw-fiat#commit-withdrawal) | `wallet:withdrawals:create` |

## Advanced Trade APIs

For trading functionality, you can also access [Advanced Trade APIs](/coinbase-app/advanced-trade-apis/overview) with OAuth2 tokens. See the [OAuth2 Access Guide](/coinbase-app/advanced-trade-apis/guides/oauth-access) for details on portfolio access.

| Endpoint                                        | Description                                                         | Scope                                                              |
| :---------------------------------------------- | :------------------------------------------------------------------ | :----------------------------------------------------------------- |
| `GET /api/v3/brokerage/accounts`                | [List trading accounts](/coinbase-app/advanced-trade-apis/rest-api) | [See guide](/coinbase-app/advanced-trade-apis/guides/oauth-access) |
| `POST /api/v3/brokerage/orders`                 | [Create orders](/coinbase-app/advanced-trade-apis/rest-api)         | [See guide](/coinbase-app/advanced-trade-apis/guides/oauth-access) |
| `GET /api/v3/brokerage/orders/historical/batch` | [List orders](/coinbase-app/advanced-trade-apis/rest-api)           | [See guide](/coinbase-app/advanced-trade-apis/guides/oauth-access) |

<Info>
  For the complete Advanced Trade API reference, see the [API Reference](/api-reference/advanced-trade-api/rest-api/accounts/list-accounts).
</Info>

<Info>
  Additional endpoints for buys, sells, and notifications are available. See the [full scopes list](/coinbase-app/oauth2-integration/scopes) for all capabilities.
</Info>

## Scopes reference

For a complete list of OAuth2 scopes and what they enable, see the [Scopes Reference](/coinbase-app/oauth2-integration/scopes).

