# ExportEvmAccountOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportEvmAccountOptions



```ts theme={null}
type ExportEvmAccountOptions = {
  evmAccount: EvmAddress;
  idempotencyKey?: string;
};
```

Request parameters for exporting an EVM account's private key.

## Properties

| Property                | Type                                                                                  | Description                                |
| ----------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| <a /> `evmAccount`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | The EVM account to export.                 |
| <a /> `idempotencyKey?` | `string`                                                                              | Optional idempotency key for safe retries. |

