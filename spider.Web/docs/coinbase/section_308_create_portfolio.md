# Create portfolio
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/create-portfolio

POST /api/v1/portfolios
Create a new portfolio. Request will fail if no name is provided or if user already has max number of portfolios. Max number of portfolios is 20.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    CreatePortfolioRequest request = new CreatePortfolioRequest.Builder()
        .name("portfolio_name")
        .build();
    CreatePortfolioResponse response = portfoliosService.createPortfolio(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new CreatePortfolioRequest(
        Name: "portfolio_name",
    );
    var response = portfoliosService.CreatePortfolio(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    ordersSvc := orders.NewOrdersService(client)
    request := &portfolios.CreatePortfolioRequest{
        Name: "portfolio_name",
    }
    response, err := portfoliosSvc.CreatePortfolio(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = CreatePortfolioRequest(
        name="portfolio_name",
    )
    response = client.create_portfolio(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.createPortfolio({
        name: 'portfolio_name',
    }).then(async (response) => {
        console.log('Portfolio Created: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl create-portfolio --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

