# useGetEvmEip7702DelegationOperation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useGetEvmEip7702DelegationOperation



```ts theme={null}
function useGetEvmEip7702DelegationOperation(): {
  getEvmEip7702DelegationOperation: (options: GetEvmEip7702DelegationOperationOptions) => Promise<EvmEip7702DelegationOperation>;
};
```

A hook for getting the status of an EIP-7702 delegation operation.
Used to check the progress of a delegation operation created via createEvmEip7702Delegation.

## Returns

An object containing the getEvmEip7702DelegationOperation function.

| Name                                 | Type                                                                                                                                                                                                                                                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `getEvmEip7702DelegationOperation()` | (`options`: [`GetEvmEip7702DelegationOperationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetEvmEip7702DelegationOperationOptions)) => `Promise`\<[`EvmEip7702DelegationOperation`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EvmEip7702DelegationOperation)> |

## Example

```tsx theme={null}
import { useGetEvmEip7702DelegationOperation } from '@coinbase/cdp-hooks';

function MyComponent() {
  const { getEvmEip7702DelegationOperation } = useGetEvmEip7702DelegationOperation();

  const handleCheckOperation = async () => {
    try {
      const operation = await getEvmEip7702DelegationOperation({
        delegationOperationId: 'op-123',
      });
      console.log('Operation status:', operation.status); // PENDING | SUBMITTED | COMPLETED | FAILED
    } catch (error) {
      console.error('Failed to get operation:', error);
    }
  };

  return <button onClick={handleCheckOperation}>Check delegation operation</button>;
}
```

