# useSignInContext
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useSignInContext



```ts theme={null}
function useSignInContext(): {
  state: SignInState;
  dispatch: Dispatch<SignInAction>;
};
```

A context for the SignIn component.

## Returns

```ts theme={null}
{
  state: SignInState;
  dispatch: Dispatch<SignInAction>;
}
```

The current state of the SignIn component.

| Name       | Type                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------- |
| `state`    | [`SignInState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInState)                  |
| `dispatch` | `Dispatch`\<[`SignInAction`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/SignInAction)> |

## Example

```tsx lines theme={null}
function EmailComponent() {
  const { state } = useSignInContext();
  return <div>Submitted email: {state.email}</div>;
}

function App() {
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <SignIn>
        <SignInTitle />
        <SignInDescription />
        <EmailComponent />
        <SignInForm />
      </SignIn>
    </CDPReactProvider>
  );
```

