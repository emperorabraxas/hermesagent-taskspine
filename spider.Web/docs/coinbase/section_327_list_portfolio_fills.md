# List portfolio fills
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills

GET /api/v1/portfolios/{portfolio}/fills
Returns all of the fills for a given portfolio.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    ListPortfolioFillsRequest request = new ListPortfolioFillsRequest.Builder()
        .portfolio("portfolio_id")
        .build();
    ListPortfolioFillsResponse response = portfoliosService.listPortfolioFills(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new ListPortfolioFillsRequest(
        Portfolio: "portfolio_id",
    );
    var response = portfoliosService.ListPortfolioFills(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.GetPortfolioFillsRequest{
        Portfolio: "portfolio_id",
    }
    response, err := portfoliosSvc.GetPortfolioFillsRequest(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListPortfolioFillsRequest(
        portfolio="portfolio_id",
    )
    response = client.list_portfolio_fills(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listPortfolioFills({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Portfolio Fills: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-portfolio-fills --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

