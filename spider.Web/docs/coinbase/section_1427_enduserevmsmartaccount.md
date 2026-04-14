# EndUserEvmSmartAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EndUserEvmSmartAccount



Information about an EVM smart account associated with an end user.

## Properties

| Property               | Type        | Description                                                                                                                                             |
| ---------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `address`        | `string`    | The address of the EVM smart account. `Pattern: ^0x[0-9a-fA-F]{40}$`                                                                                    |
| <a /> `ownerAddresses` | `string`\[] | The addresses of the EVM EOA accounts that own this smart account. Smart accounts can have multiple owners, such as when spend permissions are enabled. |
| <a /> `createdAt`      | `string`    | The date and time when the account was created, in ISO 8601 format.                                                                                     |

