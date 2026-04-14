# useGetMfaConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useGetMfaConfig



```ts theme={null}
function useGetMfaConfig(): {
  getMfaConfig: () => Promise<MfaConfig>;
};
```

A hook for getting the MFA configuration for the current project.

## Returns

An object containing the getMfaConfig function.

| Name             | Type                          |
| ---------------- | ----------------------------- |
| `getMfaConfig()` | () => `Promise`\<`MfaConfig`> |

