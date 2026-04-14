# Sign a transaction
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/solana-accounts/sign-a-transaction

post /v2/solana/accounts/{address}/sign/transaction
Signs a transaction with the given Solana account.
The unsigned transaction should be serialized into a byte array and then encoded as base64.

**Transaction types**

The following transaction types are supported:
* [Legacy transactions](https://solana-labs.github.io/solana-web3.js/classes/Transaction.html)
* [Versioned transactions](https://solana-labs.github.io/solana-web3.js/classes/VersionedTransaction.html)

The developer is responsible for ensuring that the unsigned transaction is valid, as the API will not validate the transaction.


