# Send a Solana transaction
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/solana-accounts/send-a-solana-transaction

post /v2/solana/accounts/send/transaction
Signs and sends a single Solana transaction using multiple Solana accounts. The transaction may contain contain several instructions, each of which may require signatures from different account keys.

The transaction should be serialized into a byte array and base64 encoded. The API handles recent blockhash management and fee estimation, leaving the developer to provide only the minimal set of fields necessary to send the transaction.

**Transaction types**

The following transaction types are supported:
* [Legacy transactions](https://solana.com/developers/guides/advanced/versions#current-transaction-versions)
* [Versioned transactions](https://solana.com/developers/guides/advanced/versions)

**Instruction Batching**

To batch multiple operations, include multiple instructions within a single transaction. All instructions within a transaction are executed atomically - if any instruction fails, the entire transaction fails and is rolled back.

**Network Support**

The following Solana networks are supported:
* `solana` - Solana Mainnet
* `solana-devnet` - Solana Devnet

The developer is responsible for ensuring that the unsigned transaction is valid, as the API will not validate the transaction.


