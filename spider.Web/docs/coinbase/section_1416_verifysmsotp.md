# verifySmsOTP
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/verifySmsOTP



```ts theme={null}
function verifySmsOTP(options: VerifySmsOTPOptions): Promise<VerifySmsOTPResult>;
```

Verifies the one-time password (OTP) for the sign in flow with a phone number via SMS.

## Parameters

| Parameter | Type                                                                                                    | Description                       |
| --------- | ------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `options` | [`VerifySmsOTPOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifySmsOTPOptions) | The options for the verification. |

## Returns

`Promise`\<[`VerifySmsOTPResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifySmsOTPResult)>

The result of the verification.

## Example

```typescript lines theme={null}
const result = await verifySmsOTP({
  flowId: "flow-id-from-signInWithSms",
  otp: "123456" // The OTP received in SMS
});
```

