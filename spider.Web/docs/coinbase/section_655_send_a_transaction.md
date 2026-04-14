# Send a transaction
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/evm-accounts/send-a-transaction

post /v2/evm/accounts/{address}/send/transaction
Signs a transaction with the given EVM account and sends it to the indicated supported network. This API handles nonce management and gas estimation, leaving the developer to provide only the minimal set of fields necessary to send the transaction. The transaction should be serialized as a hex string using [RLP](https://ethereum.org/en/developers/docs/data-structures-and-encoding/rlp/).

The transaction must be an [EIP-1559 dynamic fee transaction](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md).


**Transaction fields and API behavior**

- `to` *(Required)*: The address of the contract or account to send the transaction to.
- `chainId` *(Ignored)*: The value of the `chainId` field in the transaction is ignored.
  The transaction will be sent to the network indicated by the `network` field in the request body.

- `nonce` *(Optional)*: The nonce to use for the transaction. If not provided, the API will assign
   a nonce to the transaction based on the current state of the account.

- `maxPriorityFeePerGas` *(Optional)*: The maximum priority fee per gas to use for the transaction.
   If not provided, the API will estimate a value based on current network conditions.

- `maxFeePerGas` *(Optional)*: The maximum fee per gas to use for the transaction.
   If not provided, the API will estimate a value based on current network conditions.

- `gasLimit` *(Optional)*: The gas limit to use for the transaction. If not provided, the API will estimate a value
  based on the `to` and `data` fields of the transaction.

- `value` *(Optional)*: The amount of ETH, in wei, to send with the transaction.
- `data` *(Optional)*: The data to send with the transaction; only used for contract calls.
- `accessList` *(Optional)*: The access list to use for the transaction.


