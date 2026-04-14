# Get the total open position limit for the portfolio
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-the-total-open-position-limits

GET /api/v1/portfolios/{portfolio}/position-limits
Retrieves the total open position limit across instruments for a given portfolio.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listOpenPositionLimits({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Position Limits: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

