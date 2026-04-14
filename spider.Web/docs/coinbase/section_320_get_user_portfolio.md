# Get user portfolio
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-user-portfolio

GET /api/v1/portfolios/{portfolio}
Returns the user's specified portfolio.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    GetPortfolioRequest request = new GetPortfolioRequest.Builder()
        .portfolioId("portfolio_id")
        .build();
    GetPortfolioResponse response = portfoliosService.getPortfolio(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new GetPortfolioRequest(
        PortfolioId: "portfolio_id",
    );
    var response = portfoliosService.GetPortfolio(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.GetPortfolioRequest{
        PortfolioId: "portfolio_id",
    }
    response, err := portfoliosSvc.GetPortfolio(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetPortfolioRequest(
        portfolio="portfolio_id",
    )
    response = client.get_portfolio(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getPortfolio({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Portfolio: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-portfolio --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

