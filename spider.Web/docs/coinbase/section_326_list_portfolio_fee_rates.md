# List portfolio fee rates
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fee-rates

GET /api/v1/portfolios/fee-rates
Retrieves the Perpetual Future and Spot fee rate tiers for the user.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    ListPortfolioFeeRatesResponse response = portfoliosService.listPortfolioFeeRates();
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var response = portfoliosService.ListPortfolioFeeRates();
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListPortfolioFeeRatesRequest()
    response = client.list_portfolio_fee_rates(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listPortfolioFeeRates().then(async (response) => {
        console.log('Portfolio Fee Rates: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

