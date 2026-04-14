# List Portfolio Balances
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/balances/list-portfolio-balances

GET /v1/portfolios/{portfolio_id}/balances
List all balances for a specific portfolio.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    BalancesService balancesService = PrimeServiceFactory.createBalancesService(client);

    ListPortfolioBalancesRequest request = new ListPortfolioBalancesRequest.Builder("PORTFOLIO_ID_HERE").build();

    ListPortfolioBalancesResponse response = balancesService.listPortfolioBalances(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var balancesService = new BalancesService(client);

    var request = new ListPortfolioBalancesRequest("PORTFOLIO_ID_HERE");
    var response = balancesService.ListPortfolioBalances(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    balancesService := balances.NewBalancesService(client)

    request := &balances.ListPortfolioBalancesRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
    }

    response, err := balancesService.ListPortfolioBalances(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListPortfolioBalancesRequest(
            portfolio_id="PORTFOLIO_ID_HERE",
    )

    response = prime_client.list_portfolio_balances(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-portfolio-balances --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const balancesService = new BalancesService(client);

    balancesService.listPortfolioBalances({
        portfolioId: 'PORTFOLIO_ID_HERE',
        symbols: 'ETH'
    }).then(async (response) => {
        console.log('Balances: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

