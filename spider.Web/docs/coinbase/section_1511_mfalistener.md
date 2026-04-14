# MfaListener
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaListener



```ts theme={null}
type MfaListener = (context: MfaVerificationContext) => void;
```

Listener function called when MFA verification is required.
The consumer should show their custom MFA UI and call initiateMfaVerification/submitMfaVerification.

## Parameters

| Parameter | Type                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------- |
| `context` | [`MfaVerificationContext`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaVerificationContext) |

## Returns

`void`

