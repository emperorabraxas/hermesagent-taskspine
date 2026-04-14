# useLinkGoogle
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useLinkGoogle



```ts theme={null}
function useLinkGoogle(): {
  linkGoogle: () => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
};
```

A hook for linking a Google account to the current user.
This is a convenience wrapper around useLinkOAuth for Google provider.

## Returns

```ts theme={null}
{
  linkGoogle: () => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
}
```

An object containing the linkGoogle function and oauthState.

| Name           | Type                                                                                                      |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| `linkGoogle()` | () => `Promise`\<`void`>                                                                                  |
| `oauthState`   | \| `null` \| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/OAuthFlowState) |

