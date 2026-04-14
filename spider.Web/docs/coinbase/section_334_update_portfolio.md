# Update portfolio
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/update-portfolio

PUT /api/v1/portfolios/{portfolio}
Update existing user portfolio.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    UpdatePortfolioRequest request = new UpdatePortfolioRequest.Builder()
        .portfolioId("portfolio_id")
        .name("new_portfolio_name")
        .build();
    UpdatePortfolioResponse response = portfoliosService.updatePortfolio(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new UpdatePortfolioRequest(
        Portfolio: "portfolio_id",
        Name: "new_portfolio_name",
    );
    var response = portfoliosService.UpdatePortfolio(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.UpdatePortfolioRequest{
        Portfolio: "portfolio_id",
        Name: "new_portfolio_name",
    }
    response, err := portfoliosSvc.UpdatePortfolio(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = UpdatePortfolioRequest(
        portfolio="portfolio_id",
        name="new_portfolio_name",
    )
    response = client.update_portfolio(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.updatePortfolio({
        portfolio: 'PORTFOLIO_ID_HERE',
        name: 'new portfolio name',
    }).then(async (response) => {
        console.log('Updated Portfolio: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl update-portfolio --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

