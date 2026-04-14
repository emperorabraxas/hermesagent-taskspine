# useSignInReducer
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useSignInReducer



```ts theme={null}
function useSignInReducer(initialState: SignInState): [SignInState, ActionDispatch<[SignInAction]>];
```

A reducer hook for the SignIn component.

## Parameters

| Parameter      | Type                                                                                   | Description                         |
| -------------- | -------------------------------------------------------------------------------------- | ----------------------------------- |
| `initialState` | [`SignInState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInState) | The initial state of the component. |

## Returns

\[[`SignInState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInState), `ActionDispatch`\<\[[`SignInAction`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/SignInAction)]>]

The current state and dispatcher to perform actions on the state.

