# useLinkApple
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useLinkApple



```ts theme={null}
function useLinkApple(): {
  linkApple: (options?: {
     idempotencyKey?: string;
  }) => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
};
```

A hook for linking an Apple account to the current user.
This is a convenience wrapper around useLinkOAuth for Apple provider.

## Returns

```ts theme={null}
{
  linkApple: (options?: {
     idempotencyKey?: string;
  }) => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
}
```

An object containing the linkApple function and oauthState.

| Name          | Type                                                                                                      |
| ------------- | --------------------------------------------------------------------------------------------------------- |
| `linkApple()` | (`options?`: \{ `idempotencyKey?`: `string`; }) => `Promise`\<`void`>                                     |
| `oauthState`  | \| `null` \| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/OAuthFlowState) |

