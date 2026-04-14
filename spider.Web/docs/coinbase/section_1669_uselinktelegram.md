# useLinkTelegram
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useLinkTelegram



```ts theme={null}
function useLinkTelegram(): {
  linkTelegram: () => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
};
```

A hook for linking a Telegram account to the current user.
This is a convenience wrapper around useLinkOAuth for Telegram provider.

## Returns

```ts theme={null}
{
  linkTelegram: () => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
}
```

An object containing the linkTelegram function and oauthState.

| Name             | Type                                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| `linkTelegram()` | () => `Promise`\<`void`>                                                                                  |
| `oauthState`     | \| `null` \| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/OAuthFlowState) |

