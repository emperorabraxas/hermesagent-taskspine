# SwapIssuesBalance
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/SwapIssuesBalance



Details of the `fromToken` balance that the `taker` must hold. Null if the `taker` has a sufficient balance.

## Properties

| Property                | Type     | Description                                                                       |
| ----------------------- | -------- | --------------------------------------------------------------------------------- |
| <a /> `token`           | `string` | The 0x-prefixed contract address of the token. `Pattern: ^0x[a-fA-F0-9]{40}$`     |
| <a /> `currentBalance`  | `string` | The current balance of the `fromToken` held by the `taker`. `Pattern: ^\d+$`      |
| <a /> `requiredBalance` | `string` | The minimum balance of `fromToken` required to execute the swap. `Pattern: ^\d+$` |

