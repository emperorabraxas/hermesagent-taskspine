# ExportSolanaAccountOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportSolanaAccountOptions



```ts theme={null}
type ExportSolanaAccountOptions = {
  solanaAccount: SolanaAddress;
  idempotencyKey?: string;
};
```

Request parameters for exporting a Solana account's private key.

## Properties

| Property                | Type                                                                                        | Description                                |
| ----------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------ |
| <a /> `solanaAccount`   | [`SolanaAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SolanaAddress) | The Solana account to export.              |
| <a /> `idempotencyKey?` | `string`                                                                                    | Optional idempotency key for safe retries. |

