# MfaVerificationContext
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaVerificationContext



```ts theme={null}
type MfaVerificationContext = {
  methods: MfaMethod[];
};
```

Context passed to the MFA verification handler when MFA is required.

## Properties

| Property        | Type                                                                                   | Description                               |
| --------------- | -------------------------------------------------------------------------------------- | ----------------------------------------- |
| <a /> `methods` | [`MfaMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaMethod)\[] | The MFA methods the user has enrolled in. |

