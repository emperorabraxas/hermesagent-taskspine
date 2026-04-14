# useCreateEvmEip7702Delegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useCreateEvmEip7702Delegation



```ts theme={null}
function useCreateEvmEip7702Delegation(): UseCreateEvmEip7702DelegationReturnType;
```

Hook that creates an EIP-7702 delegation and then polls until the delegation operation is COMPLETED.

* data: Create result (delegationOperationId). Set when create succeeds.
* status: Delegation operation result (EvmEip7702DelegationOperation). Set when polling reaches COMPLETED.

## Returns

[`UseCreateEvmEip7702DelegationReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseCreateEvmEip7702DelegationReturnType)

createEvmEip7702Delegation, data (CreateEvmEip7702DelegationResult), status (EvmEip7702DelegationOperation), error.

## Example

```tsx theme={null}
const { createEvmEip7702Delegation, data, status, error } = useCreateEvmEip7702Delegation();
await createEvmEip7702Delegation({ address: '0x...', network: 'base-sepolia' });
// data.delegationOperationId - operation ID from create
// status - delegation operation (status.status === 'COMPLETED', status.transactionHash)
```

