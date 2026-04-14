# LinkAuthFlow
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthFlow



```ts theme={null}
function LinkAuthFlow(props: LinkAuthFlowProps): Element;
```

A component for the flow of the link auth component.

LinkAuthFlow renders the LinkAuthItems component when the view is "list" and the SignIn component when the view is "email" or "sms". It also handles the transition between the views.

## Parameters

| Parameter | Type                                                                                               | Description                               |
| --------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| `props`   | [`LinkAuthFlowProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthFlowProps) | The props for the LinkAuthFlow component. |

## Returns

`Element`

The LinkAuthFlow component.

## See

[LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth)

