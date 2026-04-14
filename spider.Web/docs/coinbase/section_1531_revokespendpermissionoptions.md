# RevokeSpendPermissionOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/RevokeSpendPermissionOptions



```ts theme={null}
type RevokeSpendPermissionOptions = {
  evmSmartAccount: EvmAddress;
  network: SpendPermissionNetwork;
  permissionHash: string;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
};
```

Input for revoking a spend permission.

## Properties

| Property                 | Type                                                                                                          | Description                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| <a /> `evmSmartAccount`  | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                         | The EVM Smart Account to revoke the spend permission for.                                                            |
| <a /> `network`          | [`SpendPermissionNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SpendPermissionNetwork) | The network to revoke the spend permission on.                                                                       |
| <a /> `permissionHash`   | `string`                                                                                                      | The hash of the spend permission to revoke.                                                                          |
| <a /> `useCdpPaymaster?` | `boolean`                                                                                                     | Whether to use the CDP Paymaster for the user operation. Only available on Base. Enabled by default on Base Sepolia. |
| <a /> `paymasterUrl?`    | `string`                                                                                                      | The URL of the paymaster to use for the user operation.                                                              |
| <a /> `idempotencyKey?`  | `string`                                                                                                      | Optional idempotency key for safe retries.                                                                           |

