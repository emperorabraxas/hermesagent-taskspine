# TokenFee
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/TokenFee



## Properties

| Property       | Type     | Description                                                                                                                                                                                                          |
| -------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `amount` | `string` | The estimated amount of the fee in atomic units of the `token`. For example, `1000000000000000` if the fee is in ETH equates to 0.001 ETH, `10000` if the fee is in USDC equates to 0.01 USDC, etc. `Pattern: ^\d+$` |
| <a /> `token`  | `string` | The contract address of the token that the fee is paid in. The address `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` is used for the native token of the network (e.g. ETH). `Pattern: ^0x[a-fA-F0-9]{40}$`           |

