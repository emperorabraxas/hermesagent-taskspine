# List Portfolios
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/portfolios/list-portfolios

GET /v1/portfolios
List all portfolios for which the current API key has read access.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = PrimeServiceFactory.createPortfoliosService(client);

    ListPortfoliosResponse response = portfoliosService.listPortfolios();
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var portfoliosService = new PortfoliosService(client);

    var response = portfoliosService.ListPortfolios();
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    portfoliosService := portfolios.NewPortfoliosService(client)

    request := &portfolios.ListPortfolios{}

    response, err := portfoliosService.ListPortfolios(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListPortfoliosRequest()

    response = prime_client.list_portfolios(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-portfolios --entity-id ENTITY_ID_HERE
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.listPortfolios().then(async (response) => {
        console.log('Portfolios: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

