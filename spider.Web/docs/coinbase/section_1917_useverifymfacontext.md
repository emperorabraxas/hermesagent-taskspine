# useVerifyMfaContext
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useVerifyMfaContext



```ts theme={null}
function useVerifyMfaContext(): VerifyMfaContextValue;
```

Hook to access the VerifyMfa context.

## Returns

[`VerifyMfaContextValue`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaContextValue)

The current state and dispatch function of the VerifyMfa component.

## See

[VerifyMfa](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfa)

## Example

```tsx theme={null}
function MfaCodeDisplay() {
  const { state } = useVerifyMfaContext();
  return <div>Code: {state.mfaCode}</div>;
}
```

