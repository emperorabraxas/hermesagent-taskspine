# Create counterparty Id
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/transfers/create-counterparty-id

POST /api/v1/transfers/create-counterparty-id

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransfersService transfersService = IntxServiceFactory.createTransfersService(client);
    CreateCounterpartyIdRequest request = new CreateCounterpartyIdRequest.Builder()
        .portfolio("portfolio_id")
        .build();
    CreateCounterpartyIdResponse response = transfersService.createCounterpartyId(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var transfersService = new TransfersService(client);
    var request = new CreateCounterpartyIdRequest(
        Portfolio: "portfolio_id",
    );
    var response = transfersService.CreateCounterpartyId(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    transfersSvc := transfers.NewTransfersService(client)
    request := &transfers.CreateCounterpartyIdRequest{
        Portfolio: "portfolio_id",
    }
    response, err := transfersSvc.CreateCounterpartyId(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = CreateCounterpartyIdRequest(
        portfolio="portfolio_id",
    )
    response = client.create_counterparty_id(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const transfersService = new TransfersService(client);

    transfersService.createCounterparty({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Counterparty created: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl create-counterparty-id --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

