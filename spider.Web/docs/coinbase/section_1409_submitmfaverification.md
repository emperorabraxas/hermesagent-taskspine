# submitMfaVerification
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/submitMfaVerification



```ts theme={null}
function submitMfaVerification(options: SubmitMfaVerificationOptions): Promise<void>;
```

Submits an MFA code to complete the verification process.

After successful verification, any pending operation that was waiting for MFA
will automatically continue.

## Parameters

| Parameter | Type                                                                                                                      | Description                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `options` | [`SubmitMfaVerificationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SubmitMfaVerificationOptions) | The options for the verification. |

## Returns

`Promise`\<`void`>

A promise that resolves if MFA verification is successful.

## Example

```typescript lines theme={null}
// TOTP verification
await submitMfaVerification({
  mfaMethod: "totp",
  mfaCode: "123456"
});

// SMS verification
await submitMfaVerification({
  mfaMethod: "sms",
  mfaCode: "654321"
});
```

