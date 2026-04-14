# SignInBackButtonProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInBackButtonProps



A button to go back to the previous step of the sign-in flow.

## See

[SignInBackButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInBackButton)

## Extends

* `HTMLAttributes`\<`HTMLButtonElement`>

## Properties

| Property         | Type                                                                                         | Description                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| <a /> `step?`    | `"verification"` \| `"credentials"`                                                          | If set, will render the back button for this step of the sign in flow, regardless of the context value. |
| <a /> `size?`    | [`ButtonSize`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonSize)       | The size of the button.                                                                                 |
| <a /> `variant?` | [`ButtonVariant`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonVariant) | The variant of the button.                                                                              |

