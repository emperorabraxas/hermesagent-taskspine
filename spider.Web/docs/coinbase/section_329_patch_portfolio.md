# Patch portfolio
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/patch-portfolio

PATCH /api/v1/portfolios/{portfolio}
Update parameters for existing portfolio

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    PatchPortfolioRequest request = new PatchPortfolioRequest.Builder().build();
    PatchPortfolioResponse response = portfoliosService.patchPortfolio(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new PatchPortfolioRequest();
    var response = portfoliosService.PatchPortfolio(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = PatchPortfolioRequest()
    response = client.patch_portfolio(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>
</Tabs>

