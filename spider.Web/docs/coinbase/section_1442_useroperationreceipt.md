# UserOperationReceipt
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/UserOperationReceipt



The receipt that contains information about the execution of user operation.

## Properties

| Property                 | Type                         | Description                                                                                                     |
| ------------------------ | ---------------------------- | --------------------------------------------------------------------------------------------------------------- |
| <a /> `revert?`          | `UserOperationReceiptRevert` | -                                                                                                               |
| <a /> `transactionHash?` | `string`                     | The hash of this transaction as 0x-prefixed string. `Pattern: ^0x[a-fA-F0-9]{64}$`                              |
| <a /> `blockHash?`       | `string`                     | The block hash of the block including the transaction as 0x-prefixed string. `Pattern: ^0x[0-9a-fA-F]{64}$\|^$` |
| <a /> `blockNumber?`     | `number`                     | The block height (number) of the block including the transaction.                                               |
| <a /> `gasUsed?`         | `string`                     | The gas used for landing this user operation.                                                                   |

