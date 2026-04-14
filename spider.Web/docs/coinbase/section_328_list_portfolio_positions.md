# List portfolio positions
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-positions

GET /api/v1/portfolios/{portfolio}/positions
Returns all of the positions for a given portfolio.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    ListPortfolioPositionsRequest request = new ListPortfolioPositionsRequest.Builder()
        .portfolio("portfolio_id")
        .build();
    ListPortfolioPositionsResponse response = portfoliosService.listPortfolioPositions(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new ListPortfolioPositionsRequest(
        Portfolio: "portfolio_id",
    );
    var response = portfoliosService.ListPortfolioPositions(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.GetPortfolioPositionsRequest{
        Portfolio: "portfolio_id",
    }
    response, err := portfoliosSvc.GetPortfolioPositions(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetPortfolioPositionsRequest(
        portfolio="portfolio_id",
    )
    response = client.get_portfolio_positions(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listPositions({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Portfolio Positions: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-portfolio-positions --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

