# Get Portfolio Commission
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/commission/get-portfolio-commission

GET /v1/portfolios/{portfolio_id}/commission
Retrieve commission associated with a given portfolio.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    CommissionService commissionService = PrimeServiceFactory.createCommissionService(client);

    GetPortfolioCommissionRequest request = new GetPortfolioCommissionRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .build();

    GetPortfolioCommissionResponse response = commissionService.getPortfolioCommission(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var commissionService = new CommissionService(client);

    var request = new GetPortfolioCommissionRequest("PORTFOLIO_ID_HERE");

    var response = commissionService.GetPortfolioCommission(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    commissionService = commission.NewCommissionService(client)

    request := &commission.GetPortfolioCommissionRequest{
        PortfolioId: "portfolio-id",
    }

    response, err := commissionService.GetPortfolioCommission(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetPortfolioCommissionRequest(
        portfolio_id="portfolio-id",
    )

    response = prime_client.get_portfolio_commission(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-commission --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const commissionService = new CommissionService(client);

    commissionService.getPortfolioCommission({
        portfolioId: 'PORTFOLIO_ID_HERE'
    }).then(async (response) => {
        console.log('Commission: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

