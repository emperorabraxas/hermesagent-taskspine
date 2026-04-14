# List portfolio balances
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-balances

GET /api/v1/portfolios/{portfolio}/balances
Returns all of the balances for a given portfolio.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    ListPortfolioBalancesRequest request = new ListPortfolioBalancesRequest.Builder()
        .portfolio("portfolio_id")
        .build();
    ListPortfolioBalancesResponse response = portfoliosService.listPortfolioBalances(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new ListPortfolioBalancesRequest(
        Portfolio: "portfolio_id",
    );
    var response = portfoliosService.ListPortfolioBalances(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.GetPortfolioBalancesRequest{
        Portfolio: "portfolio_id",
    }
    response, err := portfoliosSvc.GetPortfolioBalances(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListPortfolioBalancesResponse(
        portfolio="portfolio_id",
    )
    response = client.list_portfolio_balances(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listPortfolioBalances({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Portfolio Balances: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-portfolio-balances --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

