# WaitForEvmEip7702DelegationOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/WaitForEvmEip7702DelegationOptions



```ts theme={null}
type WaitForEvmEip7702DelegationOptions = {
  delegationOperationId: string;
  intervalMs?: number;
  timeoutMs?: number;
};
```

Options for waiting for an EIP-7702 delegation operation to complete.

## Properties

| Property                      | Type     | Description                                                                                |
| ----------------------------- | -------- | ------------------------------------------------------------------------------------------ |
| <a /> `delegationOperationId` | `string` | The unique identifier for the delegation operation returned by createEvmEip7702Delegation. |
| <a /> `intervalMs?`           | `number` | Polling interval in milliseconds. **Default** `2000`                                       |
| <a /> `timeoutMs?`            | `number` | Maximum time to wait in milliseconds before giving up. **Default** `120000 (2 minutes)`    |

