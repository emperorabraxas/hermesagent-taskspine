# VerifyMfaInlineFlowProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaInlineFlowProps



Props for VerifyMfaInlineFlow component.

## See

[VerifyMfaInlineFlow](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaInlineFlow)

## Properties

| Property               | Type                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                                                                              |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a /> `children`       | \| `ReactNode` \| (`props`: \| \{ `view`: `"verify"`; `Content`: `ReactNode`; } \| \{ `view`: `"content"`; `Content`: `null`; }) => `ReactNode` | The content to display. Can be: - A ReactNode: Used as the protected content (shown after MFA verification) - A render function: Receives `{ view, Content }` for full control over rendering When using a render function: - `view` is the current view ("verify" or "content") - `Content` is the default UI for that view (MFA form for "verify", null for "content") |
| <a /> `className?`     | `string`                                                                                                                                        | Additional class name for the transition container.                                                                                                                                                                                                                                                                                                                      |
| <a /> `animateHeight?` | `boolean`                                                                                                                                       | Whether to animate the height during transitions. **Default** `true`                                                                                                                                                                                                                                                                                                     |
| <a /> `autoFocus?`     | `boolean`                                                                                                                                       | Whether to auto focus forms. **Default** `true`                                                                                                                                                                                                                                                                                                                          |
| <a /> `transition?`    | `"fade"` \| `"slide"`                                                                                                                           | The type of transition to use between views. - "slide": Slides content left/right (default) - "fade": Fades content in/out **Default** `"slide"`                                                                                                                                                                                                                         |

