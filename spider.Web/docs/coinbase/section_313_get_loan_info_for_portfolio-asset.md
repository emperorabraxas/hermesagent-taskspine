# Get loan info for portfolio/asset
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-loan-info-for-portfolio

GET /api/v1/portfolios/{portfolio}/loans/{asset}
Retrieves the loan info for a given portfolio and asset.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getAssetLoan({
        portfolio: 'PORTFOLIO_ID_HERE',
        asset: 'ETH',
    }).then(async (response) => {
        console.log('Active Loan: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

