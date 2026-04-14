# List EVM token balances
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/onchain-data/list-evm-token-balances

get /v2/data/evm/token-balances/{network}/{address}
Lists the token balances of an EVM address on a given network. The balances include ERC-20 tokens and the native gas token (usually ETH). The response is paginated, and by default, returns 20 balances per page.

**Note:** This endpoint provides <1 second freshness from chain tip, <500ms response latency for wallets with reasonable token history, and 99.9% uptime for production use.


