# SignOutButtonProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignOutButtonProps



Props for the SignOutButton component.

## See

[SignOutButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignOutButton)

## Extends

* [`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps)

## Properties

| Property              | Type                                                                                         | Description                                                                              | Overrides              | Inherited from                                                                                                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `children?`     | `ReactNode`                                                                                  | The children to render inside the button.                                                | `ButtonProps.children` | -                                                                                                                                                                                           |
| <a /> `onSuccess?`    | () => `void`                                                                                 | A function to call when the sign-out is successful.                                      | -                      | -                                                                                                                                                                                           |
| <a /> `pendingLabel?` | `ReactNode`                                                                                  | A label to render when the button state is pending.                                      | -                      | [`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps).[`pendingLabel`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps#pendinglabel) |
| <a /> `variant?`      | [`ButtonVariant`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonVariant) | The variant of the button. Defaults to "primary".                                        | -                      | [`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps).[`variant`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps#variant)           |
| <a /> `asChild?`      | `boolean`                                                                                    | Set to true to use a custom element or component in place of the default button element. | -                      | [`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps).[`asChild`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps#aschild)           |
| <a /> `fullWidth?`    | `boolean`                                                                                    | Whether the button should be full width.                                                 | -                      | [`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps).[`fullWidth`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps#fullwidth)       |
| <a /> `isPending?`    | `boolean`                                                                                    | Whether the button state is pending.                                                     | -                      | [`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps).[`isPending`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps#ispending)       |
| <a /> `size?`         | [`ButtonSize`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonSize)       | The size of the button. Defaults to "md".                                                | -                      | [`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps).[`size`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps#size)                 |

