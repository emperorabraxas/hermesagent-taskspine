# listSpendPermissions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/listSpendPermissions



```ts theme={null}
function listSpendPermissions(options: ListSpendPermissionsOptions): Promise<ListSpendPermissionsResult>;
```

Lists spend permissions for the user's EVM Smart Account.

## Parameters

| Parameter | Type                                                                                                                    | Description                                |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `options` | [`ListSpendPermissionsOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ListSpendPermissionsOptions) | The options for listing spend permissions. |

## Returns

`Promise`\<[`ListSpendPermissionsResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ListSpendPermissionsResult)>

The result of the spend permissions listing.

## Example

```typescript lines theme={null}
const result = await listSpendPermissions({
  evmSmartAccount: "0x1234...",
  network: "base-sepolia",
  pageSize: 10
});

console.log("Found", result.spendPermissions.length, "spend permissions");
for (const permission of result.spendPermissions) {
  console.log("Permission:", permission.permissionHash, "Revoked:", permission.revoked);
}
```

