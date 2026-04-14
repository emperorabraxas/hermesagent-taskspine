# EnrollMfaContextValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaContextValue



The value of the EnrollMfa context.

## See

[useEnrollMfaContext](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useEnrollMfaContext)

## Properties

| Property                 | Type                                                                                                          | Description                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| <a /> `state`            | [`EnrollMfaState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaState)                  | The current state of the enrollment flow.           |
| <a /> `dispatch`         | `Dispatch`\<[`EnrollMfaAction`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/EnrollMfaAction)> | The dispatch function to update the state.          |
| <a /> `onEnrollSuccess?` | () => `void`                                                                                                  | The function to call when enrollment is successful. |

