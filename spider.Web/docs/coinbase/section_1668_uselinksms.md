# useLinkSms
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useLinkSms



```ts theme={null}
function useLinkSms(): {
  linkSms: (phoneNumber: string, options?: {
     idempotencyKey?: string;
   }) => Promise<{
     flowId: string;
     message: string;
  }>;
};
```

A hook for linking a SMS account to the current user.

## Returns

An object containing the linkSms function.

| Name        | Type                                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `linkSms()` | (`phoneNumber`: `string`, `options?`: \{ `idempotencyKey?`: `string`; }) => `Promise`\<\{ `flowId`: `string`; `message`: `string`; }> |

