# Get order details
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/orders/get-order-details

GET /api/v1/orders/{id}
Retrieves a single order. The order retrieved can be either active or inactive.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = IntxServiceFactory.createOrdersService(client);
    GetOrderRequest request = new GetOrderRequest.Builder()
        .id("order_id")
        .build();
    GetOrderResponse response = ordersService.getOrder(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var ordersService = new OrdersService(client);
    var request = new GetOrderRequest(
        Id: "order_id",
    );
    var response = ordersService.GetOrder(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    ordersSvc := orders.NewOrdersService(client)
    request := &orders.GetOrderRequest{
        Id: "order_id",
    }
    response, err := ordersSvc.GetOrder(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetOrderRequest(
        id="order_id",
    )
    response = client.get_order(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const ordersService = new OrdersService(client);

    ordersService.getOrder({
        portfolio: 'PORTFOLIO_ID_HERE',
        id: 'ORDER_ID_HERE'
    }).then(async (response) => {
        console.log('Order: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-order --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

