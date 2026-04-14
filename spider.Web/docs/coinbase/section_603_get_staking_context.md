# Get staking context
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/staking/get-staking-context

POST /v1/stake/context
Fetches the staking context for an address given the network, asset, address and [custom options](/staking/staking-api/introduction/api-usage#staking-options).

This API offers a point-in-time snapshot of key staking details, such as current stakeable, unstakeable, and claimable balances, which reflect the address’s staking position at the time of the request.

This information can be used to gate staking actions on your platform or to provide users with precise details on their staking positions. For example, knowing the current unstakeable balance allows you to inform users of the maximum amount they can unstake at that moment.



