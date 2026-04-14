# EnrollMfaState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaState



The state of the EnrollMfa component.

## Properties

| Property              | Type                                                                                                  | Description                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| <a /> `method`        | `"totp"` \| `"sms"`                                                                                   | The currently selected MFA method.                          |
| <a /> `methods`       | (`"totp"` \| `"sms"`)\[]                                                                              | The available MFA methods for enrollment.                   |
| <a /> `step`          | [`EnrollMfaStep`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/EnrollMfaStep)          | The current step of the enrollment flow.                    |
| <a /> `flowDirection` | `"left"` \| `"right"`                                                                                 | The direction of the flow.                                  |
| <a /> `mfaCode`       | `string`                                                                                              | The MFA code entered by the user (for verification step).   |
| <a /> `authUrl`       | `null` \| `string`                                                                                    | The otpauth:// URL for QR code generation (from initiate).  |
| <a /> `secret`        | `null` \| `string`                                                                                    | The base32-encoded secret for manual entry (from initiate). |
| <a /> `phoneNumber`   | `string`                                                                                              | The phone number for SMS MFA enrollment (E.164 format).     |
| <a /> `initiatedAt`   | `null` \| `number`                                                                                    | The timestamp when enrollment was initiated.                |
| <a /> `isExpired`     | `boolean`                                                                                             | Whether the enrollment session has expired.                 |
| <a /> `error`         | \| `null` \| `string` \| [`APIError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/APIError) | Error message or APIError object.                           |
| <a /> `isPending`     | `boolean`                                                                                             | Whether a request is pending.                               |
| <a /> `isSuccess`     | `boolean`                                                                                             | Whether the enrollment was successful.                      |

