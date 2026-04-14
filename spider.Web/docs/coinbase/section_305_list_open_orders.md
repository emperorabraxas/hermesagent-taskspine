# List open orders
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/orders/list-open-orders

GET /api/v1/orders
Returns a list of active orders resting on the order book matching the requested criteria. Does not return any rejected, cancelled, or fully filled orders as they are not active.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = IntxServiceFactory.createOrdersService(client);
    ListOrdersRequest request = new ListOrdersRequest.Builder()
        .build();
    ListOrdersResponse response = ordersService.listOrders(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var ordersService = new OrdersService(client);
    var request = new ListOrdersRequest();
    var response = ordersService.ListOrders(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    ordersSvc := orders.NewOrdersService(client)
    request := &orders.ListOpenOrdersRequest{}
    response, err := ordersSvc.ListOpenOrders(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListOpenOrdersRequest()
    response = client.list_open_orders(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const ordersService = new OrdersService(client);

    ordersService.listOpenOrders({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Open Orders: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl list-open-orders --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

