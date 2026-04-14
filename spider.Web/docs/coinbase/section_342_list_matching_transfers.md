# List matching transfers
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers

GET /api/v1/transfers

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransfersService transfersService = IntxServiceFactory.createTransfersService(client);
    ListTransfersRequest request = new ListTransfersRequest.Builder().build();
    ListTransfersResponse response = transfersService.listTransfers(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var transfersService = new TransfersService(client);
    var request = new ListTransfersRequest();
    var response = transfersService.ListTransfers(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    transfersSvc := transfers.NewTransfersService(client)
    request := &transfers.ListTransfersRequest{}
    response, err := transfersSvc.ListTransfers(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListTransfersRequest()
    response = client.list_transfers(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const transfersService = new TransfersService(client);

    transfersService.listTransfers().then(async (response) => {
        console.log('Transfers: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl list-transfers --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

