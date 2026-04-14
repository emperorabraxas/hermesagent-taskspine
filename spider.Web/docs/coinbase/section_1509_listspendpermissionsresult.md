# ListSpendPermissionsResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ListSpendPermissionsResult



```ts theme={null}
type ListSpendPermissionsResult = {
  spendPermissions: SpendPermissionResponseObject[];
  hasNextPage: boolean;
  nextPageToken?: string;
};
```

Result of listSpendPermissions.

## Properties

| Property                 | Type                               | Description                               |
| ------------------------ | ---------------------------------- | ----------------------------------------- |
| <a /> `spendPermissions` | `SpendPermissionResponseObject`\[] | The list of spend permissions.            |
| <a /> `hasNextPage`      | `boolean`                          | Whether there are more results available. |
| <a /> `nextPageToken?`   | `string`                           | The token for the next page (if any).     |

