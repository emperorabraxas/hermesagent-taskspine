# SpendPermissionPage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SpendPermissionPage



```ts theme={null}
type SpendPermissionPage = {
  spendPermissions: CoreListSpendPermissionsResult["spendPermissions"];
  hasNextPage: boolean;
  nextPageToken?: string;
};
```

A page of spend permissions.

## Properties

| Property                 | Type                                                    |
| ------------------------ | ------------------------------------------------------- |
| <a /> `spendPermissions` | `CoreListSpendPermissionsResult`\[`"spendPermissions"`] |
| <a /> `hasNextPage`      | `boolean`                                               |
| <a /> `nextPageToken?`   | `string`                                                |

