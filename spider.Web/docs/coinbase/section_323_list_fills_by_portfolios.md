# List fills by portfolios
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/list-fills-portfolio

GET /api/v1/portfolios/fills
Returns fills for specified portfolios or fills for all portfolios if none are provided.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listFills().then(async (response) => {
        console.log('Portfolio Fills: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

