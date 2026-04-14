# MfaRequiredCallback
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/MfaRequiredCallback



```ts theme={null}
type MfaRequiredCallback = (context: MfaVerificationContext) => void;
```

Callback function invoked when MFA verification is required.
The consumer should show their custom MFA UI when this is called.

This callback does not need to be memoized - the hook handles stability internally.

## Parameters

| Parameter | Type                     | Description                                                |
| --------- | ------------------------ | ---------------------------------------------------------- |
| `context` | `MfaVerificationContext` | The MFA verification context containing available methods. |

## Returns

`void`

