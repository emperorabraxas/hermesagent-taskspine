# toTransactionSigner
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/toTransactionSigner



```ts theme={null}
function toTransactionSigner(address: string): TransactionPartialSigner;
```

Converts a CDP Solana account into a Solana Kit transaction signer.
This enables the CDP account to be used with any library or framework that accepts Solana Kit transaction signers.

## Parameters

| Parameter | Type     | Description                                           |
| --------- | -------- | ----------------------------------------------------- |
| `address` | `string` | The Solana address to create a transaction signer for |

## Returns

`TransactionPartialSigner`

A transaction signer that can be used to sign transactions

