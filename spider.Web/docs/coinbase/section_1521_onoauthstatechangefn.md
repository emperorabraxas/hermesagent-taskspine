# OnOAuthStateChangeFn
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/OnOAuthStateChangeFn



```ts theme={null}
type OnOAuthStateChangeFn = (state: 
  | OAuthFlowState
  | null) => void;
```

Callback function type for OAuth state changes.

## Parameters

| Parameter | Type                                                                                                     |
| --------- | -------------------------------------------------------------------------------------------------------- |
| `state`   | \| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/OAuthFlowState) \| `null` |

## Returns

`void`

