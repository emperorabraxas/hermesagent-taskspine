# EIP712Domain
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EIP712Domain



The domain of the EIP-712 typed data.

## Properties

| Property                   | Type                | Description                                                      |
| -------------------------- | ------------------- | ---------------------------------------------------------------- |
| <a /> `name?`              | `string`            | The name of the DApp or protocol.                                |
| <a /> `version?`           | `string`            | The version of the DApp or protocol.                             |
| <a /> `chainId?`           | `number`            | The chain ID of the EVM network.                                 |
| <a /> `salt?`              | `` `0x${string}` `` | The optional 32-byte 0x-prefixed hex salt for domain separation. |
| <a /> `verifyingContract?` | `` `0x${string}` `` | The verifying contract address.                                  |

