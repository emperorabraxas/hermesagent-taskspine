# UseWaitForEvmEip7702DelegationParameters
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseWaitForEvmEip7702DelegationParameters



```ts theme={null}
type UseWaitForEvmEip7702DelegationParameters = {
  delegationOperationId?: string;
  enabled?: boolean;
};
```

Parameters for the `useWaitForEvmEip7702Delegation` hook.

## Properties

| Property                       | Type      | Description                                                                           |
| ------------------------------ | --------- | ------------------------------------------------------------------------------------- |
| <a /> `delegationOperationId?` | `string`  | The delegation operation ID to poll.                                                  |
| <a /> `enabled?`               | `boolean` | When false, polling does not run. Defaults to true when delegationOperationId is set. |

