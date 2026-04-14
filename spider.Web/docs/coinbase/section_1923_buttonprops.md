# ButtonProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps



The props for the Button component.

ButtonProps

## Extends

* `ButtonBaseProps`

## Extended by

* [`SignOutButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignOutButtonProps)

## Properties

| Property              | Type                                                                                         | Description                                                                              | Inherited from              |
| --------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------- |
| <a /> `pendingLabel?` | `ReactNode`                                                                                  | The label to display when the button is pending.                                         | -                           |
| <a /> `variant?`      | [`ButtonVariant`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonVariant) | The variant of the button. Defaults to "primary".                                        | -                           |
| <a /> `asChild?`      | `boolean`                                                                                    | Set to true to use a custom element or component in place of the default button element. | `ButtonBaseProps.asChild`   |
| <a /> `fullWidth?`    | `boolean`                                                                                    | Whether the button should be full width.                                                 | `ButtonBaseProps.fullWidth` |
| <a /> `isPending?`    | `boolean`                                                                                    | Whether the button state is pending.                                                     | `ButtonBaseProps.isPending` |
| <a /> `size?`         | [`ButtonSize`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonSize)       | The size of the button. Defaults to "md".                                                | `ButtonBaseProps.size`      |

