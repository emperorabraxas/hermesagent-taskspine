# SubmitMfaVerificationOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SubmitMfaVerificationOptions



```ts theme={null}
type SubmitMfaVerificationOptions = {
  mfaMethod: MfaMethod;
  mfaCode: string;
  idempotencyKey?: string;
};
```

Request parameters for submitMfaVerification.

## Properties

| Property                | Type                                                                                | Description                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| <a /> `mfaMethod`       | [`MfaMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaMethod) | -                                                                   |
| <a /> `mfaCode`         | `string`                                                                            | The 6-digit MFA code from the authenticator app (TOTP) or from SMS. |
| <a /> `idempotencyKey?` | `string`                                                                            | Optional idempotency key for safe retries.                          |

