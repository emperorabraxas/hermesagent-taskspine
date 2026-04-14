# SpendPermissionInput
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SpendPermissionInput



```ts theme={null}
type SpendPermissionInput = Omit<SpendPermission, "token" | "period" | "start" | "end" | "salt" | "extraData"> & {
  token:   | "eth"
     | "usdc"
     | EvmAddress;
  period?: number;
  periodInDays?: number;
  start?: Date;
  end?: Date;
  salt?: bigint;
  extraData?: Hex;
};
```

Dev-friendly input for creating a spend permission.

## Type declaration

| Name            | Type                                                                                                            | Description                                                                                                                                                            |
| --------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `token`         | \| `"eth"` \| `"usdc"` \| [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | Token symbol ("eth", "usdc") or contract address.                                                                                                                      |
| `period?`       | `number`                                                                                                        | Time duration for resetting used allowance on a recurring basis (seconds)                                                                                              |
| `periodInDays?` | `number`                                                                                                        | Time duration for resetting used allowance on a recurring basis (days) This can be used instead of `period` to specify a human-friendly value, like `periodInDays: 7`. |
| `start?`        | `Date`                                                                                                          | The start timestamp for the spend permission. Defaults to now.                                                                                                         |
| `end?`          | `Date`                                                                                                          | The end timestamp for the spend permission. Defaults to max uint48 (no expiration).                                                                                    |
| `salt?`         | `bigint`                                                                                                        | The salt for the spend permission. Defaults to random salt.                                                                                                            |
| `extraData?`    | [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Hex)                                         | The extra data for the spend permission. Defaults to "0x".                                                                                                             |

