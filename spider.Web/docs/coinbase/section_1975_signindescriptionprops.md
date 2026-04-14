# SignInDescriptionProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInDescriptionProps



The props for the SignInDescription component.

## See

[SignInDescription](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInDescription)

## Extends

* `SignInTitleAndDescriptionProps`.`HTMLAttributes`\<`HTMLElement`>

## Properties

| Property            | Type                                                                                   | Description                                                                                       | Inherited from                              |
| ------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| <a /> `as?`         | `ElementType`                                                                          | The element type to render the description as.                                                    | -                                           |
| <a /> `authMethod?` | [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod) | The auth method to render the title for.                                                          | `SignInTitleAndDescriptionProps.authMethod` |
| <a /> `step?`       | `"verification"` \| `"credentials"`                                                    | If set, will render the title for this step of the sign in flow, regardless of the context value. | `SignInTitleAndDescriptionProps.step`       |

