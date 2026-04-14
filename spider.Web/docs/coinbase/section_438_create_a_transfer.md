# Create a transfer
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/transfers-under-development/create-a-transfer

post /v2/transfers
Create a new transfer to move funds from a source to a target.
All transfers first transition to `quoted`. If `execute: false`, the transfer stays quoted until you call `/v2/transfers/{transferId}/execute`.
If `execute: true`, quoted status emits momentarily before the transfer moves to `processing`, where execution proceeds. Subscribe to the transfers webhook to  follow progress in real time instead of polling.


