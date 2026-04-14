# VerifySmsOTPOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifySmsOTPOptions



```ts theme={null}
type VerifySmsOTPOptions = {
  flowId: string;
  otp: string;
  idempotencyKey?: string;
};
```

Request parameters for verifySmsOTP.

## Properties

| Property                | Type     | Description                                |
| ----------------------- | -------- | ------------------------------------------ |
| <a /> `flowId`          | `string` | The flow ID to use in verifySmsOTP.        |
| <a /> `otp`             | `string` | The OTP to verify.                         |
| <a /> `idempotencyKey?` | `string` | Optional idempotency key for safe retries. |

