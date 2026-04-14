# Modify open order
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/orders/modify-open-order

PUT /api/v1/orders/{id}
Modifies an open order.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = IntxServiceFactory.createOrdersService(client);
    ModifyOrderRequest request = new ModifyOrderRequest.Builder()
        .id("order_id")
        .build();
    ModifyOrderResponse response = ordersService.modifyOrder(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var ordersService = new OrdersService(client);
    var request = new ModifyOrderRequest(
        Id: "order_id",
    );
    var response = ordersService.ModifyOrder(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    ordersSvc := orders.NewOrdersService(client)
    request := &orders.ModifyOrderRequest{
        Id: "order_id",
    }
    response, err := ordersSvc.ModifyOrder(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ModifyOrderRequest(
        id="order_id",
    )
    response = client.modify_order(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const ordersService = new OrdersService(client);

    ordersService.modifyOrder({
        portfolio: 'PORTFOLIO_ID_HERE',
        orderId: 'ORDER_ID_HERE',
        size: '2',
    }).then(async (response) => {
        console.log('Modified Order: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl modify-order --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

