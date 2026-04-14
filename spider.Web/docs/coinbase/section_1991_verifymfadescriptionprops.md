# VerifyMfaDescriptionProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaDescriptionProps



The props for the VerifyMfaDescription component.

## Extends

* `VerifyMfaMethodComponentProps`.`HTMLAttributes`\<`HTMLElement`>

## Properties

| Property        | Type                                                                                         | Description                                                    | Inherited from                         |
| --------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------- |
| <a /> `as?`     | `ElementType`                                                                                | The element type to render the description as.                 | -                                      |
| <a /> `method?` | `"totp"` \| `"sms"`                                                                          | The MFA method to render the title/description for.            | `VerifyMfaMethodComponentProps.method` |
| <a /> `step?`   | [`VerifyMfaStep`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/VerifyMfaStep) | If set, will render for this step regardless of context value. | `VerifyMfaMethodComponentProps.step`   |

