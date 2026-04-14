# Create order
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/orders/create-order

POST /api/v1/orders
Creates a new order.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = IntxServiceFactory.createOrdersService(client);
    CreateOrderRequest request = new CreateOrderRequest.Builder()
        .instrument("BTC-PERP")
        .side("BUY")
        .size("0.0001")
        .orderType("LIMIT")
        .price("50000")
        .tif("GTC")
        .clientOrderId("1234567890")
        .build();
    CreateOrderResponse response = ordersService.createOrder(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var ordersService = new OrdersService(client);
    var request = new CreateOrderRequest(
        Instrument: "BTC-PERP",
        Side: "BUY",
        Size: "0.0001",
        OrderType: "LIMIT",
        Price: "50000",
        Tif: "GTC",
        ClientOrderId: "1234567890",
    );
    var response = ordersService.CreateOrder(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    ordersSvc := orders.NewOrdersService(client)
    request := &orders.CreateOrderRequest{
        Instrument: "BTC-PERP",
        Side: "BUY",
        Size: "0.0001",
        OrderType: "LIMIT",
        Price: "50000",
        Tif: "GTC",
        ClientOrderId: "1234567890",
    }
    response, err := ordersSvc.CreateOrder(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = CreateOrderRequest(
        instrument="BTC-PERP",
        side="BUY",
        size="0.0001",
        order_type="LIMIT",
        price="50000",
        tif="GTC",
        client_order_id="1234567890",
    )
    response = client.create_order(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const ordersService = new OrdersService(client);

    ordersService.getOrder({
        clientOrderId: 'CLIENT_ORDER_ID_HERE',
        instrument: 'ETH-PERP',
        side: OrderSide.BUY,
        size: '0.001',
        orderType: OrderType.LIMIT,
        tif: TimeInForce.GTC,
        price: '4000',
    }).then(async (response) => {
        console.log('Order Created: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl create-order --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

