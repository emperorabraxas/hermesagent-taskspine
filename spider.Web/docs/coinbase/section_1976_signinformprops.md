# SignInFormProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInFormProps



Props for the SignInForm component.

## See

[SignInForm](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInForm)

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLElement`>, `"children"`>

## Properties

| Property           | Type                                                                                                                                                                                                   | Description                                                                                      | Overrides        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ---------------- |
| <a /> `as?`        | `ElementType`                                                                                                                                                                                          | The element type to render the form as.                                                          | -                |
| <a /> `autoFocus?` | `boolean`                                                                                                                                                                                              | If set, will auto focus the form when the component mounts and after transitions.                | `Omit.autoFocus` |
| <a /> `onSuccess?` | () => `void`                                                                                                                                                                                           | The function to call when the sign in is successful.                                             | -                |
| <a /> `step?`      | `"verification"` \| `"credentials"`                                                                                                                                                                    | If set, will render the form for this step of the sign in flow, regardless of the context value. | -                |
| <a /> `children?`  | (`props`: \{ `step`: `"verification"` \| `"credentials"`; `authMethod`: [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod); `Form`: `ReactNode`; }) => `ReactNode` | The children of the component.                                                                   | -                |

