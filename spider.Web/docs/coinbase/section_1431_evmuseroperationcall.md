# EvmUserOperationCall
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EvmUserOperationCall



## Properties

| Property                  | Type     | Description                                                                                                                                                        |
| ------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a /> `to`                | `string` | The address the call is directed to. `Pattern: ^0x[0-9a-fA-F]{40}$`                                                                                                |
| <a /> `value`             | `string` | The amount of ETH to send with the call, in wei.                                                                                                                   |
| <a /> `data`              | `string` | The call data to send. This is the hex-encoded data of the function call consisting of the method selector and the function arguments. `Pattern: ^0x[0-9a-fA-F]*$` |
| <a /> `overrideGasLimit?` | `string` | The override gas limit to use for the call instead of the bundler's estimated gas limit.                                                                           |

