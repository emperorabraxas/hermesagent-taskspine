# SpendPermission
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SpendPermission



```ts theme={null}
type SpendPermission = {
  account: EvmAddress;
  spender: EvmAddress;
  token: EvmAddress;
  allowance: bigint;
  period: number;
  start: number;
  end: number;
  salt: bigint;
  extraData: Hex;
};
```

A spend permission.

## Properties

| Property          | Type                                                                                  | Description                                                                      |
| ----------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| <a /> `account`   | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | The account address that owns the tokens                                         |
| <a /> `spender`   | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | Entity that can spend account's tokens. Can be either a Smart Account or an EOA. |
| <a /> `token`     | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | The token address.                                                               |
| <a /> `allowance` | `bigint`                                                                              | The allowance for the spend permission.                                          |
| <a /> `period`    | `number`                                                                              | The period in seconds for the spend permission.                                  |
| <a /> `start`     | `number`                                                                              | The start timestamp for the spend permission.                                    |
| <a /> `end`       | `number`                                                                              | The end timestamp for the spend permission.                                      |
| <a /> `salt`      | `bigint`                                                                              | The salt for the spend permission.                                               |
| <a /> `extraData` | [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Hex)               | The extra data for the spend permission.                                         |

