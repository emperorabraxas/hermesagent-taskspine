# Get sell options
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/onramp-offramp/get-sell-options

GET /v1/sell/options
The Sell Options API provides clients with a way to discover the available options for selling Crypto with Coinbase Offramp. It returns the supported fiat deposit currencies and available crypto assets that can be passed into the Sell Quote API. Clients should call this API periodically for each country they support and cache the response.


