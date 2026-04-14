# UseListSpendPermissionsReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseListSpendPermissionsReturnType



```ts theme={null}
type UseListSpendPermissionsReturnType = {
  data:   | SpendPermissionPage
     | undefined;
  error: Error | undefined;
  status: Status;
  refetch: () => void;
};
```

Return type for the useListSpendPermissions hook.

## Properties

| Property        | Type                                                                                                                       |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| <a /> `data`    | \| [`SpendPermissionPage`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SpendPermissionPage) \| `undefined` |
| <a /> `error`   | `Error` \| `undefined`                                                                                                     |
| <a /> `status`  | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                             |
| <a /> `refetch` | () => `void`                                                                                                               |

