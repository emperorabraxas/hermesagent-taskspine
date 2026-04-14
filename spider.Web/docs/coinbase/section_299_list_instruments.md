# List instruments
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/instruments/list-instruments

GET  /api/v1/instruments
Returns all of the instruments available for trading.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    InstrumentsService instrumentsService = IntxServiceFactory.createInstrumentsService(client);
    ListInstrumentsRequest request = new ListInstrumentsRequest.Builder().build();
    ListInstrumentsResponse response = instrumentsService.listInstruments(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var instrumentsService = new InstrumentsService(client);
    var request = new ListInstrumentsRequest();
    var response = instrumentsService.ListInstruments(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    instrumentsSvc := instruments.NewInstrumentsService(client)
    request := &instruments.ListInstrumentsRequest{}
    response, err := instrumentsSvc.ListInstruments(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListInstrumentsRequest()
    response = client.list_instruments(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const instrumentsService = new InstrumentsService(client);

    instrumentsService.listInstruments().then(async (response) => {
        console.log('Instruments: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl list-instruments --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

