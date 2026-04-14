# UseGetSwapPriceOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/UseGetSwapPriceOptions



Options for the `useGetSwapPrice` hook.

## Extends

* `Partial`\<[`GetSwapPriceOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetSwapPriceOptions)>

## Properties

| Property             | Type                                                                                            | Description                                                                                            | Inherited from        |
| -------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------- |
| <a /> `enabled?`     | `boolean`                                                                                       | Set to `false` to prevent automatic fetching even when all parameters are present. Defaults to `true`. | -                     |
| <a /> `network?`     | [`EvmSwapsNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmSwapsNetwork) | The network on which to perform the swap.                                                              | `Partial.network`     |
| <a /> `fromToken?`   | `` `0x${string}` ``                                                                             | The 0x-prefixed contract address of the token to sell.                                                 | `Partial.fromToken`   |
| <a /> `toToken?`     | `` `0x${string}` ``                                                                             | The 0x-prefixed contract address of the token to buy.                                                  | `Partial.toToken`     |
| <a /> `fromAmount?`  | `string`                                                                                        | The amount of fromToken to sell, in atomic units.                                                      | `Partial.fromAmount`  |
| <a /> `slippageBps?` | `number`                                                                                        | Maximum slippage in basis points (100 = 1%). Default is 100.                                           | `Partial.slippageBps` |
| <a /> `account?`     | `` `0x${string}` ``                                                                             | The taker account address. If omitted, auto-selected from the signed-in user's accounts.               | `Partial.account`     |

