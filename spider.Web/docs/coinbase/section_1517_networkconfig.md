# NetworkConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/NetworkConfig



```ts theme={null}
type NetworkConfig = {
  ethereum?: EthereumConfig;
  solana?: {
     createOnLogin?: boolean;
  };
};
```

Network-specific configuration.

## Properties

| Property                | Type                                                                                          | Description                                          |
| ----------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| <a /> `ethereum?`       | [`EthereumConfig`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EthereumConfig) | Ethereum/EVM account configuration.                  |
| <a /> `solana?`         | \{ `createOnLogin?`: `boolean`; }                                                             | Solana account configuration.                        |
| `solana.createOnLogin?` | `boolean`                                                                                     | Whether to automatically create an account on login. |

