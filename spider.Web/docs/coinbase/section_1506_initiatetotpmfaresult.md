# InitiateTotpMfaResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/InitiateTotpMfaResult



```ts theme={null}
type InitiateTotpMfaResult = {
  method: "totp";
  authUrl: string;
  secret: string;
};
```

Result of TOTP MFA enrollment initiation.

## Properties

| Property        | Type     | Description                                                            |
| --------------- | -------- | ---------------------------------------------------------------------- |
| <a /> `method`  | `"totp"` | The MFA method that was initiated.                                     |
| <a /> `authUrl` | `string` | The otpauth:// URL for the authenticator app (for QR code generation). |
| <a /> `secret`  | `string` | The base32-encoded TOTP secret (for manual entry).                     |

