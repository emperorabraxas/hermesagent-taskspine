# UseCreateDelegationReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseCreateDelegationReturnType



```ts theme={null}
type UseCreateDelegationReturnType = {
  createDelegation: (options: CreateDelegationOptions) => Promise<CreateDelegationResult>;
};
```

Return type of the `useCreateDelegation` hook.

## Properties

| Property                 | Type                                                                                                                                                                                                                                                        | Description                                               |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| <a /> `createDelegation` | (`options`: [`CreateDelegationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/CreateDelegationOptions)) => `Promise`\<[`CreateDelegationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/CreateDelegationResult)> | Function to create a delegation for the current end user. |

