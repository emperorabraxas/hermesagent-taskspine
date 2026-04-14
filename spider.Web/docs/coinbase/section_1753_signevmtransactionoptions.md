# SignEvmTransactionOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignEvmTransactionOptions



```ts theme={null}
type SignEvmTransactionOptions = {
  evmAccount: EvmAddress;
  transaction: AllowedEvmTransactionType;
  idempotencyKey?: string;
};
```

Request parameters for signing an EVM transaction.

## Properties

| Property                | Type                                                                                                                 | Description                                |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| <a /> `evmAccount`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/EvmAddress)                               | The EVM account to sign the message with.  |
| <a /> `transaction`     | [`AllowedEvmTransactionType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/AllowedEvmTransactionType) | The transaction to sign.                   |
| <a /> `idempotencyKey?` | `string`                                                                                                             | Optional idempotency key for safe retries. |

