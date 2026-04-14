# useLinkEmail
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useLinkEmail



```ts theme={null}
function useLinkEmail(): {
  linkEmail: (email: string, options?: {
     idempotencyKey?: string;
   }) => Promise<{
     flowId: string;
     message: string;
  }>;
};
```

A hook for linking an email account to the current user.

## Returns

An object containing the linkEmail function.

| Name          | Type                                                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `linkEmail()` | (`email`: `string`, `options?`: \{ `idempotencyKey?`: `string`; }) => `Promise`\<\{ `flowId`: `string`; `message`: `string`; }> |

