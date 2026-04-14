# Create Order
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/create-order

POST  /v1/portfolios/{portfolio_id}/order
Create an order.

<Info>
  **VWAP and TWAP**

  VWAP and TWAP orders must have a minimum notional of \$100/hr and also include these additional parameters: `limit_price`, `start_time` and `expiry_time`.
</Info>

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    OrdersService ordersService = PrimeServiceFactory.createOrdersService(client);

    CreateOrderRequest request = new CreateOrderRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .productId("ADA-USD")
        .side(OrderSide.BUY)
        .type(OrderType.MARKET)
        .baseQuantity("10.0")
        .clientOrderId(UUID.randomUUID().toString())
        .build());
    CreateOrderResponse orderResponse = ordersService.createOrder(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var ordersService = new OrdersService(client);

    var request = new CreateOrderRequest("PORTFOLIO_ID_HERE")
    {
        BaseQuantity = "5",
        LimitPrice = "0.32",
        Side = OrderSide.BUY,
        ProductId = "ADA-USD",
        Type = OrderType.LIMIT,
        ExpiryTime = new DateTimeOffset(DateTime.UtcNow.AddMinutes(5)).ToString("o"),
        ClientOrderId = Guid.NewGuid().ToString()
    };

    var createOrderResponse = orderService.CreateOrder(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    ordersService := orders.NewOrdersService(client)

    request := &orders.CreateOrderRequest{
        Order: &model.Order{
            PortfolioId:   "PORTFOLIO_ID_HERE",
            BaseQuantity:  "5",
            LimitPrice:    "0.32",
            Side:          "BUY",
            ProductId:     "ADA-USD",
            Type:          "LIMIT",
            ExpiryTime:    time.Now().UTC().Add(5 * time.Minute).Format(time.RFC3339),
            ClientOrderId: uuid.New().String(),
        },
    }

    response, err := ordersService.CreateOrder(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = CreateOrderRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        base_quantity="5",
        limit_price="0.32",
        side="BUY",
        product_id="ADA-USD",
        type="LIMIT",
        expiry_time=(datetime.datetime.now() + datetime.timedelta(minutes=5)).isoformat() + "Z",
        client_order_id=str(uuid.uuid4()),
    )

    response = prime_client.create_order(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl create-order --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const ordersService = new OrdersService(client);
    const today = new Date();

    ordersService.createOrder({
        portfolioId: "PORTFOLIO_ID_HERE",
        baseQuantity: "5",
        limitPrice: "0.32",
        side: OrderSide.BUY,
        productId: "ADA-USD",
        type: OrderType.LIMIT,
        expiryTime: date.setDate(date.getDate() + 1),
        clientOrderId: uuidv4()
    }).then(async (response) => {
        console.log('Order: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

