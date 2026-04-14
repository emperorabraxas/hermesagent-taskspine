# MFAMethods
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/MFAMethods



Information about the end user's MFA enrollments.

## Properties

| Property                             | Type             | Description                                                                                                                                                                                              |
| ------------------------------------ | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `enrollmentPromptedAt?`        | `string`         | The date and time when the end user was prompted for MFA enrollment, in ISO 8601 format. If the this field exists, and the user has no other enrolled MFA methods, then the user skipped MFA enrollment. |
| <a /> `lastVerificationCompletedAt?` | `string`         | The date and time when the end user last successfully completed an MFA verification, including enrollment, in ISO 8601 format.                                                                           |
| <a /> `totp?`                        | `MFAMethodsTotp` | An object containing information about the end user's TOTP enrollment.                                                                                                                                   |
| <a /> `sms?`                         | `MFAMethodsSms`  | An object containing information about the end user's SMS MFA enrollment.                                                                                                                                |

