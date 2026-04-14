# SendSolanaTransactionOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaTransactionOptions



```ts theme={null}
type SendSolanaTransactionOptions = {
  solanaAccount: SolanaAddress;
  network: SendSolanaTransactionWithEndUserAccountBodyNetwork;
  transaction: string;
  useCdpSponsor?: boolean;
  idempotencyKey?: string;
};
```

Request parameters for sending a Solana transaction.

## Properties

| Property                | Type                                                                                                                                                                  | Description                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| <a /> `solanaAccount`   | [`SolanaAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SolanaAddress)                                                                           | The Solana account to send the transaction with.                                                  |
| <a /> `network`         | [`SendSolanaTransactionWithEndUserAccountBodyNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaTransactionWithEndUserAccountBodyNetwork) | The network to send the transaction to.                                                           |
| <a /> `transaction`     | `string`                                                                                                                                                              | The base64 encoded transaction to send.                                                           |
| <a /> `useCdpSponsor?`  | `boolean`                                                                                                                                                             | Whether transaction fees should be sponsored by CDP. When true, CDP sponsors the transaction fee. |
| <a /> `idempotencyKey?` | `string`                                                                                                                                                              | Optional idempotency key for safe retries.                                                        |

