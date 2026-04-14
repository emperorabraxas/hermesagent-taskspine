# SendEvmTransactionOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmTransactionOptions



```ts theme={null}
type SendEvmTransactionOptions = {
  evmAccount: EvmAddress;
  network: SendEvmTransactionWithEndUserAccountBodyNetwork;
  transaction: AllowedEvmTransactionType;
  idempotencyKey?: string;
};
```

Request parameters for sending an EVM transaction.

## Properties

| Property                | Type                                                                                                                                                            | Description                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| <a /> `evmAccount`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                                                                           | The EVM account to send the transaction with. |
| <a /> `network`         | [`SendEvmTransactionWithEndUserAccountBodyNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmTransactionWithEndUserAccountBodyNetwork) | The network to send the transaction to.       |
| <a /> `transaction`     | [`AllowedEvmTransactionType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/AllowedEvmTransactionType)                                             | The transaction to send.                      |
| <a /> `idempotencyKey?` | `string`                                                                                                                                                        | Optional idempotency key for safe retries.    |

