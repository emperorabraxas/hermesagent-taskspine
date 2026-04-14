# LinkAuthModalTriggerProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthModalTriggerProps



Props for the link auth modal trigger button

## See

[LinkAuthModalTrigger](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthModalTrigger)

## Extends

* `Partial`\<`Pick`\<[`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps), `"className"` | `"fullWidth"` | `"size"` | `"style"` | `"variant"`>>

## Properties

| Property           | Type                                                                                         | Description                                                                  | Inherited from      |
| ------------------ | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------- |
| <a /> `children?`  | `ReactNode`                                                                                  | If provided, will render the children instead of the default trigger button. | -                   |
| <a /> `label?`     | `ReactNode`                                                                                  | The label to display on the trigger button.                                  | -                   |
| <a /> `size?`      | [`ButtonSize`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonSize)       | The size of the button. Defaults to "md".                                    | `Partial.size`      |
| <a /> `fullWidth?` | `boolean`                                                                                    | Whether the button should be full width.                                     | `Partial.fullWidth` |
| <a /> `variant?`   | [`ButtonVariant`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonVariant) | The variant of the button. Defaults to "primary".                            | `Partial.variant`   |

