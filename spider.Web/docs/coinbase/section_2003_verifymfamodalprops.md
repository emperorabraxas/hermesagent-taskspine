# VerifyMfaModalProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaModalProps



Props for the VerifyMfaModal component.

## See

[VerifyMfaModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaModal)

## Properties

| Property           | Type                            | Description                                                                                |
| ------------------ | ------------------------------- | ------------------------------------------------------------------------------------------ |
| <a /> `children?`  | `ReactNode`                     | If provided, will render the children instead of the default trigger button.               |
| <a /> `open?`      | `boolean`                       | Whether the modal is open. Note: if you set this, you must also set `setIsOpen`.           |
| <a /> `setIsOpen?` | (`value`: `boolean`) => `void`  | A function to set the modal's open state. Note: if you set this, you must also set `open`. |
| <a /> `onCancel?`  | () => `void`                    | A function to call when the verification is canceled.                                      |
| <a /> `onError?`   | (`error`: `Error`) => `void`    | A function to call when the verification errors.                                           |
| <a /> `onSuccess?` | (`mfaCode`: `string`) => `void` | A function to call when MFA is successful verified.                                        |

