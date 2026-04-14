# VerifyMfaFlowContextValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaFlowContextValue



The value of the MFA verification flow context.

## See

[useVerifyMfaFlow](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useVerifyMfaFlow)

## Properties

| Property               | Type                                      | Description                                            |
| ---------------------- | ----------------------------------------- | ------------------------------------------------------ |
| <a /> `back`           | () => `void`                              | A function to go back to the previous step.            |
| <a /> `direction`      | `"left"` \| `"right"`                     | The direction of the flow transition.                  |
| <a /> `selectMethod`   | (`method`: `"totp"` \| `"sms"`) => `void` | A function to select an alternate verification method. |
| <a /> `showMethodList` | () => `void`                              | A function to show the alternate methods list.         |

