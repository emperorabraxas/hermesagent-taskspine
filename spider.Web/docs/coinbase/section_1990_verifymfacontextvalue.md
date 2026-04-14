# VerifyMfaContextValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaContextValue



The context value for the VerifyMfa component.

## See

[useVerifyMfaContext](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useVerifyMfaContext)

## Properties

| Property           | Type                                                                                                          | Description                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| <a /> `onSuccess?` | (`mfaCode`: `string`) => `void`                                                                               | The function to call when verification is successful. |
| <a /> `onError?`   | (`error`: `Error`) => `void`                                                                                  | The function to call when verification errors.        |
| <a /> `state`      | [`VerifyMfaState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaState)                  | The current state of the verification flow.           |
| <a /> `dispatch`   | `Dispatch`\<[`VerifyMfaAction`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/VerifyMfaAction)> | The dispatch function to update the state.            |

