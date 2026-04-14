# Validate counterparty Id
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/transfers/validate-counterparty-id

POST /api/v1/transfers/validate-counterparty-id

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransfersService transfersService = IntxServiceFactory.createTransfersService(client);
    ValidateCounterpartyIdRequest request = new ValidateCounterpartyIdRequest.Builder()
        .counterpartyId("counterparty_id")
        .build();
    ValidateCounterpartyIdResponse response = transfersService.validateCounterpartyId(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var transfersService = new TransfersService(client);
    var request = new ValidateCounterpartyIdRequest(
        CounterpartyId: "counterparty_id",
    );
    var response = transfersService.ValidateCounterpartyId(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    transfersSvc := transfers.NewTransfersService(client)
    request := &transfers.ValidateCounterpartyIdRequest{
        CounterpartyId: "counterparty_id",
    }
    response, err := transfersSvc.ValidateCounterpartyId(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ValidateCounterpartyIdRequest(
        counterparty_id="counterparty_id",
    )
    response = client.validate_counterparty_id(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const transfersService = new TransfersService(client);

    transfersService.validateCounterparty({
        counterpartyId: 'COUNTERPARTY_ID_HERE',
    }).then(async (response) => {
        console.log('Counterparty created: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl validate-counterparty-id --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

