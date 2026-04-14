# useInitiateMfaEnrollment
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useInitiateMfaEnrollment



```ts theme={null}
function useInitiateMfaEnrollment(): {
  initiateMfaEnrollment: (options: InitiateMfaOptions) => Promise<InitiateMfaEnrollmentResult>;
};
```

A hook for initiating MFA enrollment for the current user.

## Returns

An object containing the initiateMfaEnrollment function.

| Name                      | Type                                                                           |
| ------------------------- | ------------------------------------------------------------------------------ |
| `initiateMfaEnrollment()` | (`options`: `InitiateMfaOptions`) => `Promise`\<`InitiateMfaEnrollmentResult`> |

