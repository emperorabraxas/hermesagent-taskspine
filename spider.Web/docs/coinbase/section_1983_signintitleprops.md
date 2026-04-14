# SignInTitleProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInTitleProps



The props for the SignInTitle component.

## See

[SignInTitle](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInTitle)

## Extends

* `SignInTitleAndDescriptionProps`.`HTMLAttributes`\<`HTMLElement`>

## Properties

| Property            | Type                                                                                   | Description                                                                                       | Inherited from                              |
| ------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| <a /> `as?`         | `ElementType`                                                                          | The element type to render the title as.                                                          | -                                           |
| <a /> `authMethod?` | [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod) | The auth method to render the title for.                                                          | `SignInTitleAndDescriptionProps.authMethod` |
| <a /> `step?`       | `"verification"` \| `"credentials"`                                                    | If set, will render the title for this step of the sign in flow, regardless of the context value. | `SignInTitleAndDescriptionProps.step`       |

