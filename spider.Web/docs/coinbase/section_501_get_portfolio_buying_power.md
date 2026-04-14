# Get Portfolio Buying Power
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/financing/get-portfolio-buying-power

GET /v1/portfolios/{portfolio_id}/buying_power
Returns the size of a buy trade that can be performed based on existing holdings and available credit. The result will differ for different assets due to asset specific credit configurations and caps. Note that this result is changing based on asset price fluctuations, so may be rejected when submitted.

### Supported Products

* Portfolio Margin
* Trade Finance

