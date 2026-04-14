# CreateSpendPermissionOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateSpendPermissionOptions



```ts theme={null}
type CreateSpendPermissionOptions = Omit<SpendPermissionInput, "account"> & {
  evmSmartAccount: EvmAddress;
  network: SpendPermissionNetwork;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
};
```

Input for creating a spend permission.
The permission owner is automatically detected from the current user.

## Type declaration

| Name               | Type                                                                                                          | Description                                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `evmSmartAccount`  | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                         | The EVM Smart Account to create the spend permission for.                                                            |
| `network`          | [`SpendPermissionNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SpendPermissionNetwork) | The network to create the spend permission on.                                                                       |
| `useCdpPaymaster?` | `boolean`                                                                                                     | Whether to use the CDP Paymaster for the user operation. Only available on Base. Enabled by default on Base Sepolia. |
| `paymasterUrl?`    | `string`                                                                                                      | The URL of the paymaster to use for the user operation.                                                              |
| `idempotencyKey?`  | `string`                                                                                                      | Optional idempotency key for safe retries.                                                                           |

