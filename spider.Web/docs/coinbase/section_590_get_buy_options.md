# Get buy options
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/onramp-offramp/get-buy-options

GET /v1/buy/options
The Buy Options API provides clients with a way to discover the available options for buying Crypto with Coinbase Onramp. It returns the supported fiat currencies and available crypto assets that can be passed into the Buy Quote API. Clients should call this API periodically for each country they support and cache the response.


