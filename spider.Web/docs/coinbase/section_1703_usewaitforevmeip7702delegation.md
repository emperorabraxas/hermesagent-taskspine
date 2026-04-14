# useWaitForEvmEip7702Delegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useWaitForEvmEip7702Delegation



```ts theme={null}
function useWaitForEvmEip7702Delegation(parameters: UseWaitForEvmEip7702DelegationParameters): UseWaitForEvmEip7702DelegationReturnType;
```

Hook that polls an EIP-7702 delegation operation until it reaches COMPLETED or FAILED.
Use this after creating a delegation to get the final operation result in React state.

## Parameters

| Parameter    | Type                                                                                                                                               | Description                                               |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `parameters` | [`UseWaitForEvmEip7702DelegationParameters`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseWaitForEvmEip7702DelegationParameters) | Delegation operation ID to poll, plus optional `enabled`. |

## Returns

[`UseWaitForEvmEip7702DelegationReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseWaitForEvmEip7702DelegationReturnType)

`{ data, error }` — when polling reaches COMPLETED, `data` is the EvmEip7702DelegationOperation.

## Example

```tsx theme={null}
const { data, error } = useWaitForEvmEip7702Delegation({
  delegationOperationId: 'op-123',
  enabled: !!operationId,
});
// When data is set, data.status === 'COMPLETED' and data.transactionHash may be set.
```

