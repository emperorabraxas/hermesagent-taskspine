# SignInModalProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInModalProps



Props for the SignInModal component.

## See

[SignInModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInModal)

## Properties

| Property             | Type                                                                                      | Description                                                                                           |
| -------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| <a /> `authMethods?` | [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)\[] | Filter the auth methods that are shown to the user (this still respects the CDP config auth methods). |
| <a /> `children?`    | `ReactNode`                                                                               | If provided, will render the children instead of the default trigger button.                          |
| <a /> `open?`        | `boolean`                                                                                 | Whether the modal is open. Note: if you set this, you must also set `setIsOpen`.                      |
| <a /> `setIsOpen?`   | (`value`: `boolean`) => `void`                                                            | A function to set the modal's open state. Note: if you set this, you must also set `open`.            |
| <a /> `onSuccess?`   | () => `void`                                                                              | A function to call when the sign-in flow is successful.                                               |

