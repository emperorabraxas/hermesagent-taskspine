# Get Portfolio Credit Information
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/financing/get-portfolio-credit-information

GET  /v1/portfolios/{portfolio_id}/credit
Retrieve a portfolio's post-trade credit information.

### Supported Products

* Trade Finance

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = PrimeServiceFactory.createPortfoliosService(client);

    GetPortfolioCreditInformationRequest request = new GetPortfolioCreditInformationRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .build();

    GetPortfolioCreditInformationResponse response = portfoliosService.getPortfolioCreditInformation(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var portfoliosService = new PortfoliosService(client);

    var request = new GetPortfolioCreditInformationRequest("PORTFOLIO_ID_HERE");

    var response = portfoliosService.GetPortfolioCreditInformation(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    portfoliosService := portfolios.NewPortfoliosService(client)

    request := &portfolios.GetPortfolioCreditInformationRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
    }

    response, err := portfoliosService.GetPortfolioCreditInformation(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetPortfolioCreditInformationRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
    )

    response = prime_client.get_portfolio_credit_information(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-credit --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getPortfolioCredit({
        portfolioId: 'PORTFOLIO_ID_HERE'
    }).then(async (response) => {
        console.log('Portfolio Credit: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

