# VerifyMfaImageProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaImageProps



The props for the VerifyMfaImage component.

## Extends

* `VerifyMfaMethodComponentProps`.`HTMLAttributes`\<`HTMLElement`>

## Properties

| Property        | Type                                                                                         | Description                                                    | Inherited from                         |
| --------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------- |
| <a /> `as?`     | `ElementType`                                                                                | -                                                              | -                                      |
| <a /> `method?` | `"totp"` \| `"sms"`                                                                          | The MFA method to render the title/description for.            | `VerifyMfaMethodComponentProps.method` |
| <a /> `step?`   | [`VerifyMfaStep`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/VerifyMfaStep) | If set, will render for this step regardless of context value. | `VerifyMfaMethodComponentProps.step`   |

