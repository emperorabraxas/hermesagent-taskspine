# UseRevokeSpendPermissionReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseRevokeSpendPermissionReturnType



```ts theme={null}
type UseRevokeSpendPermissionReturnType = {
  revokeSpendPermission: (options: RevokeSpendPermissionOptions) => Promise<RevokeSpendPermissionResult>;
  data:   | GetUserOperationResult
     | undefined;
  error: Error | undefined;
  status: Status;
};
```

Return type for the useRevokeSpendPermission hook.

## Param

The function to revoke a spend permission.

## Properties

| Property                      | Type                                                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a /> `revokeSpendPermission` | (`options`: [`RevokeSpendPermissionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/RevokeSpendPermissionOptions)) => `Promise`\<`RevokeSpendPermissionResult`> |
| <a /> `data`                  | \| [`GetUserOperationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetUserOperationResult) \| `undefined`                                                     |
| <a /> `error`                 | `Error` \| `undefined`                                                                                                                                                               |
| <a /> `status`                | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                                                                                       |

