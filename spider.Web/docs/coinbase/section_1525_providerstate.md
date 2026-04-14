# ProviderState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ProviderState



```ts theme={null}
type ProviderState = {
  chainId: number;
  setChainId: (chainId: number) => void;
  chains: readonly [Chain, ...Chain[]];
  user:   | User
     | null;
  setUser: (user: 
     | User
    | null) => void;
};
```

The attributes/methods representing the state of the provider

## Properties

| Property           | Type                                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| <a /> `chainId`    | `number`                                                                                                   |
| <a /> `setChainId` | (`chainId`: `number`) => `void`                                                                            |
| <a /> `chains`     | readonly \[`Chain`, `...Chain[]`]                                                                          |
| <a /> `user`       | \| [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/User) \| `null`                     |
| <a /> `setUser`    | (`user`: \| [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/User) \| `null`) => `void` |

