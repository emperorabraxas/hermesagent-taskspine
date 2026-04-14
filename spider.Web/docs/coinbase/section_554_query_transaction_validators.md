# Query Transaction Validators
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/staking/list-transaction-validators

post /v1/portfolios/{portfolio_id}/staking/transaction-validators/query
List ETH 0x02 validators associated with wallet-level stake transactions for a given portfolio. It will not return data for unstake transactions, portfolio stake transactions, transactions which staked different currencies, or which staked to Ethereum 0x01 validators.


