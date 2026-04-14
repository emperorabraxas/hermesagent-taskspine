# Get latest staking operation
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/staking/get-latest-staking-operation

GET /v1/networks/{network_id}/addresses/{address_id}/staking_operations/{staking_operation_id}
Fetches the latest staking operation for the specified network and address given the staking operation ID.

This API can be used to poll the status of a staking operation and check if it has been successfully completed or not.

A completed staking operation will have a status of `completed` which is indicative of the fact that all staking transactions have been successfully created and no more staking transactions will be generated.



