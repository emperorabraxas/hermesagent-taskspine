# Sign a transaction
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/evm-accounts/sign-a-transaction

post /v2/evm/accounts/{address}/sign/transaction
Signs a transaction with the given EVM account.
The transaction should be serialized as a hex string using [RLP](https://ethereum.org/en/developers/docs/data-structures-and-encoding/rlp/).

The transaction must be an [EIP-1559 dynamic fee transaction](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md). The developer is responsible for ensuring that the unsigned transaction is valid, as the API will not validate the transaction.


