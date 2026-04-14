# EnrollMfa
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfa



```ts theme={null}
function EnrollMfa(props: EnrollMfaProps): Element;
```

A component for MFA enrollment. Guides users through setting up
two-factor authentication.

## Parameters

| Parameter | Type                                                                                         | Description                  |
| --------- | -------------------------------------------------------------------------------------------- | ---------------------------- |
| `props`   | [`EnrollMfaProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaProps) | The props for the component. |

## Returns

`Element`

The rendered component.

## Examples

```tsx theme={null}
// Default usage
<EnrollMfa onEnrollSuccess={() => console.log("Enrolled!")} />
```

```tsx theme={null}
// With custom UI
<EnrollMfa onEnrollSuccess={onEnrollSuccess}>
  {(state) => (
    <>
      <h1>{state.step === "list" ? "Multi-factor authentication" : "Add new method"}</h1>
      <EnrollMfaTitle />
      <EnrollMfaDescription />
      {state.step === "list" && <EnrollMfaError />}
      <EnrollMfaFlow />
    </>
  )}
</EnrollMfa>
```

## Further reading

* [EnrollMfa Overview](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfa.README)

