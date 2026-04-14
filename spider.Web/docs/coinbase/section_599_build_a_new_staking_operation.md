# Build a new staking operation
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/staking/build-a-new-staking-operation

POST /v1/stake/build
Builds a new staking operation containing a dynamic list of staking transactions based on the specified network, asset, address, and [custom options](/staking/staking-api/introduction/api-usage#staking-options).

It returns a StakingOperation resource, a unified interface for the entire staking process. Regardless of network complexity, the API abstracts away all the underlying details through it.
You can iterate through this resource to access each staking transaction and have them be signed and broadcasted to land the staking transaction onchain.

Read up more about the stake operation and how to interact with it [here](/staking/staking-api/introduction/the-staking-operation).



