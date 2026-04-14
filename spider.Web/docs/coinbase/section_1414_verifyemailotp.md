# verifyEmailOTP
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/verifyEmailOTP



```ts theme={null}
function verifyEmailOTP(options: VerifyEmailOTPOptions): Promise<VerifyEmailOTPResult>;
```

Verifies the one-time password (OTP) for the sign in flow with an email.

## Parameters

| Parameter | Type                                                                                                        | Description                       |
| --------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `options` | [`VerifyEmailOTPOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyEmailOTPOptions) | The options for the verification. |

## Returns

`Promise`\<[`VerifyEmailOTPResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyEmailOTPResult)>

The result of the verification.

## Example

```typescript lines theme={null}
const result = await verifyEmailOTP({
  flowId: "flow-id-from-signInWithEmail",
  otp: "123456" // The OTP received in email
});
```

