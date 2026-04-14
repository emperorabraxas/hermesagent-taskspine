# List active loans for the portfolio
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/list-active-loans-for-the-portfolio

GET /api/v1/portfolios/{portfolio}/loans
Retrieves all loan info for a given portfolio.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listActiveLoans({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Active Loans: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

