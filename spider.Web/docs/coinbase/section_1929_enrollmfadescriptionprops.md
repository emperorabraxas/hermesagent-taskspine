# EnrollMfaDescriptionProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaDescriptionProps



The props for the EnrollMfaDescription component.

## Extends

* `EnrollMfaMethodComponentProps`.`HTMLAttributes`\<`HTMLElement`>

## Properties

| Property        | Type                                                                                         | Description                                                    | Inherited from                         |
| --------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------- |
| <a /> `as?`     | `ElementType`                                                                                | The element type to render the description as.                 | -                                      |
| <a /> `method?` | `"totp"` \| `"sms"`                                                                          | The MFA method to render for.                                  | `EnrollMfaMethodComponentProps.method` |
| <a /> `step?`   | [`EnrollMfaStep`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/EnrollMfaStep) | If set, will render for this step regardless of context value. | `EnrollMfaMethodComponentProps.step`   |

