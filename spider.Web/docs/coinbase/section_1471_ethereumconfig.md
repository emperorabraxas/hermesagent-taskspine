# EthereumConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EthereumConfig



```ts theme={null}
type EthereumConfig = 
  | {
  createOnLogin?: "smart";
  enableSpendPermissions?: boolean;
}
  | {
  createOnLogin?: "eoa";
};
```

The configuration for the Ethereum account.

## Type declaration

```ts theme={null}
{
  createOnLogin?: "smart";
  enableSpendPermissions?: boolean;
}
```

| Name                      | Type      | Description                                                                                                                                                                                                            |
| ------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `createOnLogin?`          | `"smart"` | -                                                                                                                                                                                                                      |
| `enableSpendPermissions?` | `boolean` | Whether to enable spend permissions for the smart account. Setting this to true is necessary in order to create spend permissions. Only new accounts can be created with spend permissions enabled. Defaults to false. |

```ts theme={null}
{
  createOnLogin?: "eoa";
}
```

| Name             | Type    |
| ---------------- | ------- |
| `createOnLogin?` | `"eoa"` |

