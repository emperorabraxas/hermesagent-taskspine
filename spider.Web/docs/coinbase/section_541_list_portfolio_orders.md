# List Portfolio Orders
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/list-portfolio-orders

GET  /v1/portfolios/{portfolio_id}/orders
List historical orders for a given portfolio. This endpoint returns a payload with a default limit of 100 if not specified by the user. The maximum allowed limit is 3000. <br /><br />**Caution:** Currently, you cannot query open orders with this endpoint: use List Open Orders if you have less than 1000 open orders, otherwise use Websocket API, or FIX API to stream open orders.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = PrimeServiceFactory.createOrdersService(client);

    ListOrdersRequest request = new ListOrdersRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .build();

    ListOrdersResponse response = ordersService.listOrders(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var ordersService = new OrdersService(client);

    var request = new ListOrdersRequest("PORTFOLIO_ID_HERE");

    var response = ordersService.ListOrders(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    ordersService := orders.NewOrdersService(client)

    request := &orders.ListOrdersRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
    }

    response, err := ordersService.ListOrders(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListOrdersRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
    )

    response = prime_client.list_orders(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-orders --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const ordersService = new OrdersService(client);

    ordersService.listPortfolioOrders({
        portfolioId: 'PORTFOLIO_ID_HERE'
    }).then(async (response) => {
        console.log('Orders: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

