# InitiateMfaVerificationOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/InitiateMfaVerificationOptions



```ts theme={null}
type InitiateMfaVerificationOptions = {
  mfaMethod: MfaMethod;
  idempotencyKey?: string;
};
```

Request parameters for initiating MFA verification.

## Properties

| Property                | Type                                                                                | Description                                 |
| ----------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------- |
| <a /> `mfaMethod`       | [`MfaMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaMethod) | The MFA method to verify ("totp" or "sms"). |
| <a /> `idempotencyKey?` | `string`                                                                            | Optional idempotency key for safe retries.  |

