# UseWaitForUserOperationReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseWaitForUserOperationReturnType



```ts theme={null}
type UseWaitForUserOperationReturnType = {
  status: Status;
  data:   | GetUserOperationResult
     | undefined;
  error: Error | undefined;
};
```

Represents the return type of the `useWaitForUserOperation` hook.

## Properties

| Property       | Type                                                                                                                             |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `status` | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                                   |
| <a /> `data`   | \| [`GetUserOperationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetUserOperationResult) \| `undefined` |
| <a /> `error`  | `Error` \| `undefined`                                                                                                           |

