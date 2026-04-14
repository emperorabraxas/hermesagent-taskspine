# SignEvmTypedDataOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignEvmTypedDataOptions



```ts theme={null}
type SignEvmTypedDataOptions = {
  evmAccount: EvmAddress;
  typedData: EIP712TypedData;
  idempotencyKey?: string;
};
```

Request parameters for signing EIP-712 typed data with an EVM account.

## Properties

| Property                | Type                                                                                           | Description                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------- |
| <a /> `evmAccount`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/EvmAddress)         | The EVM account to sign the typed data with. |
| <a /> `typedData`       | [`EIP712TypedData`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/EIP712TypedData) | The EIP-712 typed data to sign.              |
| <a /> `idempotencyKey?` | `string`                                                                                       | Optional idempotency key for safe retries.   |

