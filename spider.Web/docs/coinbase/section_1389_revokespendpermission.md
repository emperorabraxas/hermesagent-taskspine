# revokeSpendPermission
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/revokeSpendPermission



```ts theme={null}
function revokeSpendPermission(options: RevokeSpendPermissionOptions): Promise<RevokeSpendPermissionResult>;
```

Revokes a spend permission for the user's EVM Smart Account.

## Parameters

| Parameter | Type                                                                                                                      | Description                                    |
| --------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `options` | [`RevokeSpendPermissionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/RevokeSpendPermissionOptions) | The options for revoking the spend permission. |

## Returns

`Promise`\<[`RevokeSpendPermissionResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/RevokeSpendPermissionResult)>

The result of the spend permission revocation.

## Example

```typescript lines theme={null}
const result = await revokeSpendPermission({
  evmSmartAccount: "0x1234...",
  network: "base-sepolia",
  permissionHash: "0x5678...",
  useCdpPaymaster: true
});

console.log("User Operation Hash:", result.userOperationHash);
```

