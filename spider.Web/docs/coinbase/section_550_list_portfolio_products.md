# List Portfolio Products
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/products/list-portfolio-products

GET /v1/portfolios/{portfolio_id}/products
List tradable products for a given portfolio.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    ProductsService productsService = PrimeServiceFactory.createProductsService(client);

    ListPortfolioProductsRequest request = new ListPortfolioProductsRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .build();

    ListPortfolioProductsResponse response = productsService.listPortfolioProducts(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var productsService = new ProductsService(client);

    var request = new ListPortfolioProductsRequest("PORTFOLIO_ID_HERE");

    var response = productsService.ListPortfolioProducts(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    productsService := products.NewProductsService(client)

    request := &products.ListProducts{
        PortfolioId: "PORTFOLIO_ID_HERE",
    }

    response, err := productsService.ListProducts(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListProducts(
        portfolio_id="PORTFOLIO_ID_HERE",
    )

    response = prime_client.list_products(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-products --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const productsService = new ProductsService(client);

    productsService.listProducts({
        portfolioId: 'PORTFOLIO_ID_HERE'
    }).then(async (response) => {
        console.log('Products: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

