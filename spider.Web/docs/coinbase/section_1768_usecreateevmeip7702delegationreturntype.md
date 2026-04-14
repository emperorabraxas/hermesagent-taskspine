# UseCreateEvmEip7702DelegationReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseCreateEvmEip7702DelegationReturnType



```ts theme={null}
type UseCreateEvmEip7702DelegationReturnType = {
  createEvmEip7702Delegation: (options: CreateEvmEip7702DelegationOptions) => Promise<CreateEvmEip7702DelegationResult>;
  data: CreateEvmEip7702DelegationResult | undefined;
  status:   | EvmEip7702DelegationOperationResult
     | undefined;
  error: Error | undefined;
};
```

Return type of the `useCreateEvmEip7702Delegation` hook.

* data: CreateEvmEip7702DelegationResult (delegationOperationId).
* status: EvmEip7702DelegationOperationResult (operation status).

## Properties

| Property                           | Type                                                                                                                                                                                                | Description                                                                                      |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| <a /> `createEvmEip7702Delegation` | (`options`: [`CreateEvmEip7702DelegationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/CreateEvmEip7702DelegationOptions)) => `Promise`\<`CreateEvmEip7702DelegationResult`> | -                                                                                                |
| <a /> `data`                       | `CreateEvmEip7702DelegationResult` \| `undefined`                                                                                                                                                   | Create result (delegation operation ID). Set when create succeeds.                               |
| <a /> `status`                     | \| [`EvmEip7702DelegationOperationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/EvmEip7702DelegationOperationResult) \| `undefined`                                          | Delegation operation result (EvmEip7702DelegationOperation). Set when polling reaches COMPLETED. |
| <a /> `error`                      | `Error` \| `undefined`                                                                                                                                                                              | -                                                                                                |

