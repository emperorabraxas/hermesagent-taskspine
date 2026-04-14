# UseSendUserOperationReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseSendUserOperationReturnType



```ts theme={null}
type UseSendUserOperationReturnType = {
  sendUserOperation: (options: SendUserOperationOptions) => Promise<SendUserOperationResult>;
  data:   | GetUserOperationResult
     | undefined;
  error: Error | undefined;
  status: Status;
};
```

Represents the return type of the `useSendUserOperation` hook.

## Properties

| Property                  | Type                                                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `sendUserOperation` | (`options`: `SendUserOperationOptions`) => `Promise`\<`SendUserOperationResult`>                                                 |
| <a /> `data`              | \| [`GetUserOperationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetUserOperationResult) \| `undefined` |
| <a /> `error`             | `Error` \| `undefined`                                                                                                           |
| <a /> `status`            | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                                   |

