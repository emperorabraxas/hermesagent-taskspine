# List Open Orders
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/list-open-orders

GET /v1/portfolios/{portfolio_id}/open_orders
List all open orders. <br /><br />**Caution:** The maximum number of orders returned is 5000. If a client has more than 5000 open orders, an error is returned prompting the user to use Websocket API, or FIX API to stream open orders.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = PrimeServiceFactory.createOrdersService(client);

    ListOpenOrdersRequest request = new ListOpenOrdersRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .build();

    ListOpenOrdersResponse response = ordersService.listOpenOrders(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var ordersService = new OrdersService(client);

    var request = new ListOpenOrdersRequest("PORTFOLIO_ID_HERE");

    var response = ordersService.ListOpenOrders(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    ordersService := orders.NewOrdersService(client)

    request := &orders.ListOpenOrdersRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
    }

    response, err := ordersService.ListOpenOrders(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListOpenOrdersRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
    )

    response = prime_client.list_open_orders(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-open-orders --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const ordersService = new OrdersService(client);

    ordersService.listOpenOrders({
        portfolioId: 'PORTFOLIO_ID_HERE'
    }).then(async (response) => {
        console.log('Orders: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

