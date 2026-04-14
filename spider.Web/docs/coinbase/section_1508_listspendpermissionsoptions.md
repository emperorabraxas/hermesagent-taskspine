# ListSpendPermissionsOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ListSpendPermissionsOptions



```ts theme={null}
type ListSpendPermissionsOptions = {
  evmSmartAccount: EvmAddress;
  network: SpendPermissionNetwork;
  pageSize?: number;
  pageToken?: string;
};
```

Input for listing spend permissions.

## Properties

| Property                | Type                                                                                                          | Description                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| <a /> `evmSmartAccount` | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                         | The EVM Smart Account to list spend permissions for. |
| <a /> `network`         | [`SpendPermissionNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SpendPermissionNetwork) | The network to list spend permissions from.          |
| <a /> `pageSize?`       | `number`                                                                                                      | The number of spend permissions to return per page.  |
| <a /> `pageToken?`      | `string`                                                                                                      | The token for the next page of spend permissions.    |

