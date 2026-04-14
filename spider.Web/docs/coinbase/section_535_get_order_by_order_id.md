# Get Order by Order ID
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/get-order-by-order-id

GET /v1/portfolios/{portfolio_id}/orders/{order_id}
Retrieve an order by order ID.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = PrimeServiceFactory.createOrdersService(client);

    GetOrderByOrderIdRequest request = new GetOrderByOrderIdRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .orderId("ORDER_ID_HERE")
        .build();

    GetOrderByOrderIdResponse response = ordersService.getOrderByOrderId(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var ordersService = new OrdersService(client);

    var request = new GetOrderByOrderIdRequest("PORTFOLIO_ID_HERE", "ORDER_ID_HERE");

    var response = ordersService.GetOrderByOrderId(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    ordersService := orders.NewOrdersService(client)

    request := &orders.GetOrderRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        OrderId: "ORDER_ID_HERE",
    }

    response, err := ordersService.GetOrder(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetOrderRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        order_id="ORDER_ID_HERE",
    )

    response = prime_client.get_order(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-order --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const ordersService = new OrdersService(client);

    ordersService.getOrder({
        portfolioId: 'PORTFOLIO_ID_HERE',
        orderId: 'ORDER_ID_HERE'
    }).then(async (response) => {
        console.log('Order: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

