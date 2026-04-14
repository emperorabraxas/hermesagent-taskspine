# List Solana token balances
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/solana-token-balances/list-solana-token-balances

get /v2/solana/token-balances/{network}/{address}
Lists the token balances of a Solana address on a given network. The balances include SPL tokens and the native SOL token. The response is paginated, and by default, returns 20 balances per page.

**Note:** This endpoint is still under development and does not yet provide strong availability or freshness guarantees. Freshness and availability of new token balances will improve over the coming weeks.


