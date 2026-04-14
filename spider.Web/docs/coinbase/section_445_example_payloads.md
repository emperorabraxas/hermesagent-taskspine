# Example payloads
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/transfers/example-payloads



Use this page to quickly compare transfer `source` and `target` payload examples.

## Supported resource types

| Endpoint                                                                                                                    | `source` allowed types                                                                                                                                                                   | `target` allowed types                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Create transfer request](/api-reference/payment-apis/rest-api/transfers-under-development/create-a-transfer)               | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)                        | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)<br />- Onchain address<br />- Email address |
| [Get transfers](/api-reference/payment-apis/rest-api/transfers-under-development/list-transfers)                            | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)<br />- Onchain address | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)<br />- Onchain address<br />- Email address |
| [Get transfer by ID](/api-reference/payment-apis/rest-api/transfers-under-development/get-a-transfer)                       | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)<br />- Onchain address | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)<br />- Onchain address<br />- Email address |
| [Transfer webhook event payloads](/api-reference/payment-apis/rest-api/transfers-under-development/transfer-status-changed) | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)<br />- Onchain address | - [Account](/api-reference/payment-apis/rest-api/accounts/accounts)<br />- [Payment Method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)<br />- Onchain address<br />- Email address |

## Example payloads

### Source

An example of a `source` payload using a payment method:

```json theme={null}
{
  "source": {
    "paymentMethodId": "pm_...",
    "asset": "usd"
  }
}
```

### Target

An example of a `target` payload using an onchain address:

```json theme={null}
{
  "target": {
    "address": "0x...",
    "network": "base",
    "asset": "usdc"
  }
}
```

## Type-specific examples

### Onchain address

An example onchain address object used in transfer payloads:

```json theme={null}
{
  "address": "0x...",
  "network": "base",
  "asset": "usdc"
}
```

### Email address

An example email address object used in transfer target payloads:

```json theme={null}
{
  "email": "recipient@example.com",
  "asset": "usd"
}
```

### Deposit destination in `details`

An example deposit destination reference in transfer or webhook payloads:

```json theme={null}
{
  "details": {
    "depositDestination": {
      "id": "depositDestination_..."
    }
  }
}
```

<Note>
  This page shows examples for `source` and `target` only.

  [Deposit destinations](/api-reference/payment-apis/rest-api/deposit-destinations-under-development/overview) are returned separately in `details.depositDestination.id` (not inside `source` or `target`).

  See [Webhooks sample transfer event payloads](/api-reference/payment-apis/webhooks/example-payloads) for a full deposit-data example.
</Note>

