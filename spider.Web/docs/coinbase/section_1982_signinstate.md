# SignInState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInState



The state of the SignIn component.

## See

* [SignIn](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignIn)
* [useSignInReducer](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useSignInReducer)

## Properties

| Property            | Type                                                                                                  | Description                              |
| ------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| <a /> `authMethod`  | [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)                | The auth method selected by the user.    |
| <a /> `authMethods` | [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)\[]             | -                                        |
| <a /> `canResetOTP` | `boolean`                                                                                             | Whether the user can request a new OTP.  |
| <a /> `email`       | `string`                                                                                              | The email address of the user.           |
| <a /> `error`       | \| `null` \| `string` \| [`APIError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/APIError) | The error message or APIError object.    |
| <a /> `flowId`      | `string`                                                                                              | The flow ID of the current sign-in flow. |
| <a /> `isPending`   | `boolean`                                                                                             | Whether the form state is pending.       |
| <a /> `isSuccess`   | `boolean`                                                                                             | Whether the sign-in flow is successful.  |
| <a /> `otp`         | `string`                                                                                              | The OTP code entered by the user.        |
| <a /> `phoneNumber` | `string`                                                                                              | The phone number of the user.            |
| <a /> `step`        | `"verification"` \| `"credentials"`                                                                   | The current step of the sign-in flow.    |

