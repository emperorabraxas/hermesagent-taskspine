# SignEvmHashOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmHashOptions



```ts theme={null}
type SignEvmHashOptions = {
  evmAccount: EvmAddress;
  hash: Hex;
  idempotencyKey?: string;
};
```

Request parameters for signing a hash with an EVM account.

## Properties

| Property                | Type                                                                                  | Description                                |
| ----------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| <a /> `evmAccount`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | The EVM account to sign the hash with.     |
| <a /> `hash`            | [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Hex)               | The hash to sign.                          |
| <a /> `idempotencyKey?` | `string`                                                                              | Optional idempotency key for safe retries. |

