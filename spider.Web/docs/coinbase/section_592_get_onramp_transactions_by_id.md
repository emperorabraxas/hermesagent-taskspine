# Get onramp transactions by ID
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/onramp-offramp/get-onramp-transactions-by-id

GET /v1/buy/user/{partnerUserRef}/transactions
When you initialize the Onramp Widget you can pass a `partnerUserRef` parameter to associate the transaction created during that session with the ID. You can then use that ID in this API to retrieve that transaction and any others that share the ID. The value of the `partnerUserRef` param can be any string you want e.g. the ID of the user in your app, a unique transaction ID, or a combination of values. Anything that is meaningful to your app.


