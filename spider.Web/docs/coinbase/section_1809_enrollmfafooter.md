# EnrollMfaFooter
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaFooter



```ts theme={null}
function EnrollMfaFooter(props: HTMLAttributes<HTMLDivElement>): Element;
```

A footer component for the MFA enrollment flow.

## Parameters

| Parameter | Type                                | Description                  |
| --------- | ----------------------------------- | ---------------------------- |
| `props`   | `HTMLAttributes`\<`HTMLDivElement`> | The props for the component. |

## Returns

`Element`

The rendered footer.

## Example

```tsx theme={null}
<EnrollMfa>
  <EnrollMfaTitle />
  <EnrollMfaDescription />
  <EnrollMfaForm />
  <EnrollMfaFooter />
</EnrollMfa>
```

