# VerifyMfaFooter
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaFooter



```ts theme={null}
function VerifyMfaFooter(props: HTMLAttributes<HTMLDivElement>): Element;
```

A footer component for the MFA verification flow.

## Parameters

| Parameter | Type                                | Description                  |
| --------- | ----------------------------------- | ---------------------------- |
| `props`   | `HTMLAttributes`\<`HTMLDivElement`> | The props for the component. |

## Returns

`Element`

The rendered footer.

## Example

```tsx theme={null}
<VerifyMfa>
  <VerifyMfaTitle />
  <VerifyMfaDescription />
  <VerifyMfaFlow />
  <VerifyMfaFooter />
</VerifyMfa>
```

