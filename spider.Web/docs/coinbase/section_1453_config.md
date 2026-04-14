# Config
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Config



```ts theme={null}
type Config = BaseConfig & {
  ethereum?: NetworkConfig["ethereum"];
  solana?: NetworkConfig["solana"];
};
```

Configuration for the core package with at least one network specified.

## Type declaration

| Name        | Type                                                                                                       | Description                         |
| ----------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `ethereum?` | [`NetworkConfig`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/NetworkConfig)\[`"ethereum"`] | Ethereum/EVM account configuration. |
| `solana?`   | [`NetworkConfig`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/NetworkConfig)\[`"solana"`]   | Solana account configuration.       |

