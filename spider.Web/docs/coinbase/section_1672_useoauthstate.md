# useOAuthState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useOAuthState



```ts theme={null}
function useOAuthState(): {
  oauthState:   | null
     | OAuthFlowState;
};
```

Hook to access the current OAuth flow state.
This can be used to track the status of an ongoing OAuth authentication flow.

## Returns

```ts theme={null}
{
  oauthState:   | null
     | OAuthFlowState;
}
```

The current OAuth flow state

| Name         | Type                                                                                                      |
| ------------ | --------------------------------------------------------------------------------------------------------- |
| `oauthState` | \| `null` \| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/OAuthFlowState) |

## Example

```tsx lines theme={null}
function OAuthStatus() {
  const { oauthState } = useOAuthState();

  if (!oauthState) {
    return null;
  }

  return (
    <div>
      <p>OAuth Status: {oauthState.status}</p>
      {oauthState.status === "error" && (
        <p>Error: {oauthState.errorDescription}</p>
      )}
    </div>
  );
}
```

