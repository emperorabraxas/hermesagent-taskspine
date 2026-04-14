# InitiateTotpMfaOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/InitiateTotpMfaOptions



```ts theme={null}
type InitiateTotpMfaOptions = {
  mfaMethod: "totp";
  idempotencyKey?: string;
};
```

Request parameters for initiating TOTP MFA enrollment.

## Properties

| Property                | Type     | Description                                |
| ----------------------- | -------- | ------------------------------------------ |
| <a /> `mfaMethod`       | `"totp"` | The MFA method to use.                     |
| <a /> `idempotencyKey?` | `string` | Optional idempotency key for safe retries. |

