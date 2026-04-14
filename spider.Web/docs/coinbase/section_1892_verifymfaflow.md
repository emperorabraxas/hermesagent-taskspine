# VerifyMfaFlow
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaFlow



```ts theme={null}
function VerifyMfaFlow(props: VerifyMfaFlowProps): Element;
```

The flow for the VerifyMfa component. Renders the appropriate content
based on the current MFA method and step.

The "verification" step renders the current method's content (verification form).
The "list" step renders alternate method options.

## Parameters

| Parameter | Type                                                                                                 | Description          |
| --------- | ---------------------------------------------------------------------------------------------------- | -------------------- |
| `props`   | [`VerifyMfaFlowProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaFlowProps) | The component props. |

## Returns

`Element`

The rendered component.

## Example

```tsx theme={null}
<VerifyMfa>
  <VerifyMfaTitle />
  <VerifyMfaDescription />
  <VerifyMfaFlow />
</VerifyMfa>
```

