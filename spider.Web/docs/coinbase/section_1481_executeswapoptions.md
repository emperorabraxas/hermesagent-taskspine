# ExecuteSwapOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExecuteSwapOptions



```ts theme={null}
type ExecuteSwapOptions = {
  network: EvmSwapsNetwork;
  fromToken: EvmAddress;
  toToken: EvmAddress;
  fromAmount: string;
  slippageBps?: number;
  account?: EvmAddress;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
};
```

Request parameters for executing a token swap.

## Properties

| Property                 | Type                                                                                            | Description                                                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `network`          | [`EvmSwapsNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmSwapsNetwork) | The network on which to perform the swap.                                                                                                               |
| <a /> `fromToken`        | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)           | The 0x-prefixed contract address of the token to sell.                                                                                                  |
| <a /> `toToken`          | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)           | The 0x-prefixed contract address of the token to buy.                                                                                                   |
| <a /> `fromAmount`       | `string`                                                                                        | The amount of fromToken to sell, in atomic units.                                                                                                       |
| <a /> `slippageBps?`     | `number`                                                                                        | Maximum slippage in basis points (100 = 1%). Default is 100.                                                                                            |
| <a /> `account?`         | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)           | The taker account address. If omitted, auto-selected from the signed-in user's accounts.                                                                |
| <a /> `useCdpPaymaster?` | `boolean`                                                                                       | Whether to use the CDP Paymaster for gas sponsorship. Only applicable for smart accounts; ignored for EOA. Cannot be used together with `paymasterUrl`. |
| <a /> `paymasterUrl?`    | `string`                                                                                        | Custom paymaster URL for gas sponsorship. Only applicable for smart accounts; ignored for EOA. Cannot be used together with `useCdpPaymaster`.          |
| <a /> `idempotencyKey?`  | `string`                                                                                        | Optional idempotency key for safe retries.                                                                                                              |

