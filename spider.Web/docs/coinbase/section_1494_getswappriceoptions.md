# GetSwapPriceOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetSwapPriceOptions



```ts theme={null}
type GetSwapPriceOptions = {
  network: EvmSwapsNetwork;
  fromToken: EvmAddress;
  toToken: EvmAddress;
  fromAmount: string;
  slippageBps?: number;
  account?: EvmAddress;
};
```

Request parameters for getting an indicative swap price.

## Properties

| Property             | Type                                                                                            | Description                                                                              |
| -------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| <a /> `network`      | [`EvmSwapsNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmSwapsNetwork) | The network on which to perform the swap.                                                |
| <a /> `fromToken`    | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)           | The 0x-prefixed contract address of the token to sell.                                   |
| <a /> `toToken`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)           | The 0x-prefixed contract address of the token to buy.                                    |
| <a /> `fromAmount`   | `string`                                                                                        | The amount of fromToken to sell, in atomic units.                                        |
| <a /> `slippageBps?` | `number`                                                                                        | Maximum slippage in basis points (100 = 1%). Default is 100.                             |
| <a /> `account?`     | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)           | The taker account address. If omitted, auto-selected from the signed-in user's accounts. |

