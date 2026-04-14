# calculateSecureIframeHeight
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/calculateSecureIframeHeight



```ts theme={null}
function calculateSecureIframeHeight(theme?: Partial<SecureIframeTheme>): number;
```

Calculates the height of the secure iframe based on button size and font size.

## Parameters

| Parameter | Type                                                                                                            | Description                                        |
| --------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `theme?`  | `Partial`\<[`SecureIframeTheme`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeTheme)> | Optional theme with buttonSize and buttonFontSize. |

## Returns

`number`

The calculated height in pixels.

