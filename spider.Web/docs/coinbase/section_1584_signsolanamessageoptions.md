# SignSolanaMessageOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignSolanaMessageOptions



```ts theme={null}
type SignSolanaMessageOptions = {
  solanaAccount: SolanaAddress;
  message: string;
  idempotencyKey?: string;
};
```

Request parameters for signing a message with a Solana account.

## Properties

| Property                | Type                                                                                        | Description                                  |
| ----------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------- |
| <a /> `solanaAccount`   | [`SolanaAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SolanaAddress) | The Solana account to sign the message with. |
| <a /> `message`         | `string`                                                                                    | The message to sign (base64 encoded).        |
| <a /> `idempotencyKey?` | `string`                                                                                    | Optional idempotency key for safe retries.   |

