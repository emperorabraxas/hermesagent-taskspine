# useCreateDelegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useCreateDelegation



```ts theme={null}
function useCreateDelegation(): UseCreateDelegationReturnType;
```

Hook that provides a function to create a delegation allowing a developer to sign on behalf of an end user.

## Returns

[`UseCreateDelegationReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseCreateDelegationReturnType)

An object containing the createDelegation function.

## Example

```tsx theme={null}
const { createDelegation } = useCreateDelegation();
const result = await createDelegation({ expiresAt: '2025-12-31T23:59:59Z' });
console.log(result.delegationId);
```

