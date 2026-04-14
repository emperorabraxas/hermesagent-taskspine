# VerifyMfaState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaState



The state of the VerifyMfa component.

## Properties

| Property              | Type                                                                                                  | Description                                                                |
| --------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| <a /> `method`        | `"totp"` \| `"sms"`                                                                                   | The currently selected MFA method.                                         |
| <a /> `methods`       | (`"totp"` \| `"sms"`)\[]                                                                              | The available MFA methods for verification (from user's enrolled methods). |
| <a /> `step`          | [`VerifyMfaStep`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/VerifyMfaStep)          | The current step of the verification flow.                                 |
| <a /> `flowDirection` | `"left"` \| `"right"`                                                                                 | The direction of the flow transition.                                      |
| <a /> `mfaCode`       | `string`                                                                                              | The MFA code entered by the user.                                          |
| <a /> `error`         | \| `null` \| `string` \| [`APIError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/APIError) | Error message or APIError object.                                          |
| <a /> `isPending`     | `boolean`                                                                                             | Whether a verification request is pending.                                 |
| <a /> `isSuccess`     | `boolean`                                                                                             | Whether the verification was successful.                                   |

