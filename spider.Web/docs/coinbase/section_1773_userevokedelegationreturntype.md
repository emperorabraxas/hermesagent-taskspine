# UseRevokeDelegationReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseRevokeDelegationReturnType



```ts theme={null}
type UseRevokeDelegationReturnType = {
  revokeDelegation: (options?: RevokeDelegationOptions) => Promise<void>;
};
```

Return type of the `useRevokeDelegation` hook.

## Properties

| Property                 | Type                                                                                                                                                 | Description                                                         |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| <a /> `revokeDelegation` | (`options?`: [`RevokeDelegationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/RevokeDelegationOptions)) => `Promise`\<`void`> | Function to revoke all active delegations for the current end user. |

