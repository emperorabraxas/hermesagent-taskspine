# List EVM token balances
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/evm-token-balances/list-evm-token-balances

get /v2/evm/token-balances/{network}/{address}
Lists the token balances of an EVM address on a given network. The balances include ERC-20 tokens and the native gas token (usually ETH). The response is paginated, and by default, returns 20 balances per page.
**Note:** This endpoint is still under development and does not yet provide strong freshness guarantees. Specifically, balances of new tokens can, on occasion, take up to ~30 seconds to appear, while balances of tokens already belonging to an address will generally be close to chain tip. Freshness of new token balances will improve over the coming weeks.


