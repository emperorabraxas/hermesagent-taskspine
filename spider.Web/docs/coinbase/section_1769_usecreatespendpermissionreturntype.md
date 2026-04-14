# UseCreateSpendPermissionReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseCreateSpendPermissionReturnType



```ts theme={null}
type UseCreateSpendPermissionReturnType = {
  createSpendPermission: (options: CreateSpendPermissionOptions) => Promise<CreateSpendPermissionResult>;
  data:   | GetUserOperationResult
     | undefined;
  error: Error | undefined;
  status: Status;
};
```

Return type for the useCreateSpendPermission hook.

## Param

The function to create a spend permission.

## Properties

| Property                      | Type                                                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a /> `createSpendPermission` | (`options`: [`CreateSpendPermissionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/CreateSpendPermissionOptions)) => `Promise`\<`CreateSpendPermissionResult`> |
| <a /> `data`                  | \| [`GetUserOperationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetUserOperationResult) \| `undefined`                                                     |
| <a /> `error`                 | `Error` \| `undefined`                                                                                                                                                               |
| <a /> `status`                | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                                                                                       |

