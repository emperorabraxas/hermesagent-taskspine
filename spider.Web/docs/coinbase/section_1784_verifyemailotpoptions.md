# VerifyEmailOTPOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/VerifyEmailOTPOptions



```ts theme={null}
type VerifyEmailOTPOptions = {
  flowId: string;
  otp: string;
  idempotencyKey?: string;
};
```

Request parameters for verifyEmailOTP.

## Properties

| Property                | Type     | Description                                |
| ----------------------- | -------- | ------------------------------------------ |
| <a /> `flowId`          | `string` | The flow ID to use in verifyEmailOTP.      |
| <a /> `otp`             | `string` | The OTP to verify.                         |
| <a /> `idempotencyKey?` | `string` | Optional idempotency key for safe retries. |

