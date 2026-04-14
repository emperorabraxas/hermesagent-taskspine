# Request to stake currency in a portfolio
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/staking/request-to-stake-currency-in-a-portfolio

post /v1/portfolios/{portfolio_id}/staking/initiate
Creates an execution request to stake funds across a portfolio.  This will stake funds in one or more wallets in the portfolio, with a total bondable balance up to the requested stake amount.


