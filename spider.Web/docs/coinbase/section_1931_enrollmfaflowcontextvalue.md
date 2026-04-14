# EnrollMfaFlowContextValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaFlowContextValue



The value of the MFA enrollment flow context.

## See

[useEnrollMfaFlow](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useEnrollMfaFlow)

## Properties

| Property                | Type                                                  | Description                                  |
| ----------------------- | ----------------------------------------------------- | -------------------------------------------- |
| <a /> `back`            | () => `void`                                          | A function to go back to the previous step.  |
| <a /> `startEnrollment` | (`method`: `"totp"` \| `"sms"`) => `Promise`\<`void`> | A function to start enrollment for a method. |
| <a /> `submit`          | (`e`: `FormEvent`\<`HTMLFormElement`>) => `void`      | A function to submit the MFA code.           |

