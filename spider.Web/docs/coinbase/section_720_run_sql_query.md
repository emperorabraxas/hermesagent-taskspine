# Run SQL Query
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/sql-api/run-sql-query

post /v2/data/query/run
Run a read-only SQL query against indexed blockchain data including transactions, events, and decoded logs.

This endpoint provides direct SQL access to comprehensive blockchain data across supported networks.

Queries are executed against optimized data structures for high-performance analytics.

### Allowed Queries

  - Standard SQL syntax (CoinbaSeQL dialect, based on ClickHouse dialect)
  - Read-only queries (SELECT statements)
  - No DDL or DML operations
  - Query that follow limits (defined below)

### Supported Tables

  - `<network>.events` - Base mainnet decoded event logs with parameters, event signature, topics, and more.
  - `<network>.transactions` - Base mainnet transaction data including hash, block number, gas usage.
  - `<network>.blocks` - Base mainnet block information.
  - `<network>.encoded_logs` - Encoded log data of event logs that aren't able to be decoded by our event decoder (ex: log0 opcode).
  - `<network>.decoded_user_operations` - Decoded user operations data including hash, block number, gas usage, builder codes, entrypoint version, and more.
  - `<network>.transaction_attributions` - Information about the attributions of a transaction to a builder and associated builder codes.

### Supported Networks

  - Base Mainnet: `base`
  - Base Sepolia: `base_sepolia`

  So for example, valid tables are: `base.events`, `base_sepolia.events`, `base.transactions`, etc.

### Query Limits

  - Maximum result set: 50,000 rows
  - Maximum query length: 10,000 characters
  - Maximum on-disk data to read: 100GB
  - Maximum memory usage: 15GB
  - Query timeout: 30 seconds
  - Maximum JOINs: 12

### Query Caching

By default, each query result is returned from cache so long as the result is from an identical query and less than 750ms old. This freshness tolerance can be modified upwards, to a maximum of 900000ms (i.e. 900s, 15m).
This can be helpful for users who wish to reduce expensive calls to the SQL API by reusing cached results.



