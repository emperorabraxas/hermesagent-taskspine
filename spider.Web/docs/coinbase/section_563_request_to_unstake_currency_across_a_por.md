# Request to unstake currency across a portfolio
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/staking/request-to-unstake-currency-portfolio

POST /v1/portfolios/{portfolio_id}/staking/unstake
Creates an execution request to unstake funds across a portfolio.  This will unstake funds in one or more wallets in the portfolio, with a total bonded balance up to the requested unstake amount.


