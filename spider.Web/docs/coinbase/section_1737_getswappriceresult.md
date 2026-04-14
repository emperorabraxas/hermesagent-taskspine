# GetSwapPriceResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetSwapPriceResult



```ts theme={null}
type GetSwapPriceResult = {
  liquidityAvailable: true;
  network: EvmSwapsNetwork;
  fromToken: string;
  fromAmount: string;
  toToken: string;
  toAmount: string;
  minToAmount: string;
  fees:   | SwapFees
     | null;
  issues:   | SwapIssues
     | null;
  totalNetworkFee: string | null;
};
```

Returned when liquidity is available for the requested swap.

## Properties

| Property                   | Type                                                                                                | Description                                                                                                                                                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `liquidityAvailable` | `true`                                                                                              | Always true when this type is returned.                                                                                                                                                                                    |
| <a /> `network`            | [`EvmSwapsNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmSwapsNetwork)     | The network.                                                                                                                                                                                                               |
| <a /> `fromToken`          | `string`                                                                                            | The fromToken address.                                                                                                                                                                                                     |
| <a /> `fromAmount`         | `string`                                                                                            | The fromAmount in atomic units.                                                                                                                                                                                            |
| <a /> `toToken`            | `string`                                                                                            | The toToken address.                                                                                                                                                                                                       |
| <a /> `toAmount`           | `string`                                                                                            | Expected output at current market price, in atomic units.                                                                                                                                                                  |
| <a /> `minToAmount`        | `string`                                                                                            | Minimum output after slippage, in atomic units.                                                                                                                                                                            |
| <a /> `fees`               | \| [`SwapFees`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SwapFees) \| `null`     | Fees to be deducted in this transaction, or null.                                                                                                                                                                          |
| <a /> `issues`             | \| [`SwapIssues`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SwapIssues) \| `null` | Preflight issues (e.g. insufficient allowance or balance) that may prevent execution, or null.                                                                                                                             |
| <a /> `totalNetworkFee`    | `string` \| `null`                                                                                  | The estimated total network cost of the swap. On chains where there is no L1 data cost, it is calculated as gas \* gasPrice. On chains where there is an L1 data cost, it is calculated as gas \* gasPrice + L1 data cost. |

