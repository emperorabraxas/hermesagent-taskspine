# Get Entity Payment Method
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/payment-methods/get-entity-payment-method

GET /v1/entities/{entity_id}/payment-methods/{payment_method_id}
Get payment method details by id for a given entity.

<Info>
  **Entity ID**

  To retrieve your entity\_id, use [List Portfolios](/api-reference/prime-api/rest-api/portfolios/list-portfolios).
</Info>

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PaymentMethodsService paymentMethodsService = PrimeServiceFactory.createPaymentMethodsService(client);

    GetEntityPaymentMethodRequest request = new GetEntityPaymentMethodRequest.Builder()
        .entityId("ENTITY_ID_HERE")
        .paymentMethodId("PAYMENT_METHOD_ID_HERE")
        .build();

    GetEntityPaymentMethodResponse response = paymentMethodsService.getEntityPaymentMethod(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var paymentMethodsService = new PaymentMethodsService(client);

    var request = new GetEntityPaymentMethodRequest("ENTITY_ID_HERE", "PAYMENT_METHOD_ID_HERE");

    var response = paymentMethodsService.GetEntityPaymentMethod(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    paymentMethodsService := paymentmethods.NewPaymentMethodsService(client)

    request := &paymentmethods.GetEntityPaymentMethodRequest{
        Id: "ENTITY_ID_HERE",
        PaymentMethodId: "PAYMENT_METHOD_ID_HERE",
    }

    response, err := paymentMethodsService.GetEntityPaymentMethod(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetEntityPaymentMethodRequest(
        entity_id="ENTITY_ID_HERE",
        payment_method_id="PAYMENT_METHOD_ID_HERE",
    )

    response = prime_client.get_entity_payment_method(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-entity-payment-method --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const paymentMethodsService = new PaymentMethodsService(client);

    paymentMethodsService.getPaymentMethod({
        entityId: 'ENTITY_ID_HERE',
        paymentMethodId: 'PAYMENT_METHOD_ID_HERE'
    }).then(async (response) => {
        console.log('Payment Methods: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

