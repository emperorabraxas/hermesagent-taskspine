# SwitchEthereumChainRequest
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwitchEthereumChainRequest



```ts theme={null}
type SwitchEthereumChainRequest = {
  method: "wallet_switchEthereumChain";
  params: [{
     chainId: string;
  }];
};
```

A request to switch to the specified Ethereum chain

## Properties

| Property       | Type                           |
| -------------- | ------------------------------ |
| <a /> `method` | `"wallet_switchEthereumChain"` |
| <a /> `params` | \[\{ `chainId`: `string`; }]   |

