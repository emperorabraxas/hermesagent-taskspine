# VerifyMfa
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfa



```ts theme={null}
function VerifyMfa(props: VerifyMfaProps): Element;
```

A component for MFA verification. Prompts enrolled users to enter their
authenticator code.

## Parameters

| Parameter | Type                                                                                         | Description                  |
| --------- | -------------------------------------------------------------------------------------------- | ---------------------------- |
| `props`   | [`VerifyMfaProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaProps) | The props for the component. |

## Returns

`Element`

The rendered component.

## Examples

```tsx theme={null}
// Default usage
<VerifyMfa onSuccess={(mfaCode) => console.log("Verified!", mfaCode)} />
```

```tsx theme={null}
// With custom UI
<VerifyMfa onSuccess={handleSuccess}>
  {(state) => (
    <>
      <h2>Enter your code</h2>
      <VerifyMfaFlow />
      {state.error && <p className="error">{state.error}</p>}
    </>
  )}
</VerifyMfa>
```

## Further reading

* [VerifyMfa Overview](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfa.README)

