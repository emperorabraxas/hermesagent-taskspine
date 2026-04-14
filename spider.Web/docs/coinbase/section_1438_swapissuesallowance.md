# SwapIssuesAllowance
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/SwapIssuesAllowance



Details of the allowance that the `taker` must set in order to execute the swap successfully. Null if no allowance is required.

## Properties

| Property                 | Type     | Description                                                                     |
| ------------------------ | -------- | ------------------------------------------------------------------------------- |
| <a /> `currentAllowance` | `string` | The current allowance of the `fromToken` by the `taker`. `Pattern: ^\d+$`       |
| <a /> `spender`          | `string` | The 0x-prefixed address to set the allowance on. `Pattern: ^0x[a-fA-F0-9]{40}$` |

