# useInitiateMfaVerification
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useInitiateMfaVerification



```ts theme={null}
function useInitiateMfaVerification(): {
  initiateMfaVerification: (options: InitiateMfaVerificationOptions) => Promise<void>;
};
```

A hook for initiating MFA verification for sensitive operations.

## Returns

An object containing the initiateMfaVerification function.

| Name                        | Type                                                                |
| --------------------------- | ------------------------------------------------------------------- |
| `initiateMfaVerification()` | (`options`: `InitiateMfaVerificationOptions`) => `Promise`\<`void`> |

