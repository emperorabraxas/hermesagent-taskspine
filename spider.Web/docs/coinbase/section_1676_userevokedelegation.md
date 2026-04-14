# useRevokeDelegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useRevokeDelegation



```ts theme={null}
function useRevokeDelegation(): UseRevokeDelegationReturnType;
```

Hook that provides a function to revoke all active delegations for the current end user.

## Returns

[`UseRevokeDelegationReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseRevokeDelegationReturnType)

An object containing the revokeDelegation function.

## Example

```tsx theme={null}
const { revokeDelegation } = useRevokeDelegation();
await revokeDelegation();
```

