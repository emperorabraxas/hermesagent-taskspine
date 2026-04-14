# EnrollMfaImageProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaImageProps



The props for the EnrollMfaImage component.

## Extends

* `EnrollMfaMethodComponentProps`.`HTMLAttributes`\<`HTMLElement`>

## Properties

| Property        | Type                                                                                         | Description                                                    | Inherited from                         |
| --------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------- |
| <a /> `as?`     | `ElementType`                                                                                | -                                                              | -                                      |
| <a /> `method?` | `"totp"` \| `"sms"`                                                                          | The MFA method to render for.                                  | `EnrollMfaMethodComponentProps.method` |
| <a /> `step?`   | [`EnrollMfaStep`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/EnrollMfaStep) | If set, will render for this step regardless of context value. | `EnrollMfaMethodComponentProps.step`   |

