# SignSolanaTransactionOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignSolanaTransactionOptions



```ts theme={null}
type SignSolanaTransactionOptions = {
  solanaAccount: SolanaAddress;
  transaction: string;
  idempotencyKey?: string;
};
```

Request parameters for signing a Solana transaction.

## Properties

| Property                | Type                                                                                        | Description                                      |
| ----------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <a /> `solanaAccount`   | [`SolanaAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SolanaAddress) | The Solana account to sign the transaction with. |
| <a /> `transaction`     | `string`                                                                                    | The base64 encoded transaction to sign.          |
| <a /> `idempotencyKey?` | `string`                                                                                    | Optional idempotency key for safe retries.       |

