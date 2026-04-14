# List Order Fills
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/list-order-fills

GET /v1/portfolios/{portfolio_id}/orders/{order_id}/fills
Retrieve fills on a given order. This endpoint returns a payload with a default limit of 100 if not specified by the user. The maximum allowed limit is 3000.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = PrimeServiceFactory.createOrdersService(client);

    ListOrderFillsRequest request = new ListOrderFillsRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .orderId("ORDER_ID_HERE")
        .build();

    ListOrderFillsResponse response = ordersService.listOrderFills(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var ordersService = new OrdersService(client);

    var request = new ListOrderFillsRequest("PORTFOLIO_ID_HERE", "ORDER_ID_HERE");

    var response = ordersService.ListOrderFills(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    ordersService := orders.NewOrdersService(client)

    request := &orders.ListOrderFillsRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        OrderId: "ORDER_ID_HERE",
    }

    response, err := ordersService.ListOrderFills(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListOrderFillsRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        order_id="ORDER_ID_HERE",
    )

    response = prime_client.list_order_fills(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-order-fills --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const ordersService = new OrdersService(client);

    ordersService.listOrderFills({
        portfolioId: 'PORTFOLIO_ID_HERE',
        orderId: 'ORDER_ID_HERE',
    }).then(async (response) => {
        console.log('Fills: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

