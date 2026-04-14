# EnrollMfaModalProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaModalProps



Props for the EnrollMfaModal component.

## See

[EnrollMfaModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaModal)

## Extends

* `Pick`\<[`EnrollMfaProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaProps), `"onEnrollSuccess"` | `"resetOnSuccess"`>

## Properties

| Property                 | Type                           | Description                                                                                  | Inherited from         |
| ------------------------ | ------------------------------ | -------------------------------------------------------------------------------------------- | ---------------------- |
| <a /> `children?`        | `ReactNode`                    | If provided, will render the children instead of the default trigger button.                 | -                      |
| <a /> `open?`            | `boolean`                      | Whether the modal is open. Note: if you set this, you must also set `setIsOpen`.             | -                      |
| <a /> `setIsOpen?`       | (`value`: `boolean`) => `void` | A function to set the modal's open state. Note: if you set this, you must also set `open`.   | -                      |
| <a /> `onEnrollSuccess?` | () => `void`                   | A function to call when the enrollment is successful.                                        | `Pick.onEnrollSuccess` |
| <a /> `resetOnSuccess?`  | `boolean`                      | Whether to reset the enrollment state when the enrollment is successful. Defaults to `true`. | `Pick.resetOnSuccess`  |

