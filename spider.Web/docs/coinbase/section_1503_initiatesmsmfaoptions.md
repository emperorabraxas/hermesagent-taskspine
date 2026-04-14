# InitiateSmsMfaOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/InitiateSmsMfaOptions



```ts theme={null}
type InitiateSmsMfaOptions = {
  mfaMethod: "sms";
  phoneNumber: string;
  idempotencyKey?: string;
};
```

Request parameters for initiating SMS MFA enrollment.

## Properties

| Property                | Type     | Description                                                                                                                                                |
| ----------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `mfaMethod`       | `"sms"`  | The MFA method to use.                                                                                                                                     |
| <a /> `phoneNumber`     | `string` | Phone number in E.164 format (e.g., +14155552671). You can use any phone number for SMS MFA, even if it differs from your SMS authentication phone number. |
| <a /> `idempotencyKey?` | `string` | Optional idempotency key for safe retries.                                                                                                                 |

