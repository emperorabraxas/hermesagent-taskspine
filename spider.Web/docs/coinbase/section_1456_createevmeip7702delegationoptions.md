# CreateEvmEip7702DelegationOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateEvmEip7702DelegationOptions



```ts theme={null}
type CreateEvmEip7702DelegationOptions = {
  address: EvmAddress;
  network: EvmEip7702DelegationNetwork;
  enableSpendPermissions?: boolean;
  idempotencyKey?: string;
};
```

Options for creating an EIP-7702 delegation for an EVM EOA account.

## Properties

| Property                        | Type                                                                                                                    | Description                                                                                                                                                                              |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `address`                 | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                                   | The 0x-prefixed address of the EVM EOA account to delegate. Must belong to the current user.                                                                                             |
| <a /> `network`                 | [`EvmEip7702DelegationNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmEip7702DelegationNetwork) | The network to create the delegation on.                                                                                                                                                 |
| <a /> `enableSpendPermissions?` | `boolean`                                                                                                               | Whether to configure spend permissions for the upgraded, delegated account. When enabled, the account can grant permissions for third parties to spend on its behalf. Defaults to false. |
| <a /> `idempotencyKey?`         | `string`                                                                                                                | Optional idempotency key for safe retries.                                                                                                                                               |

