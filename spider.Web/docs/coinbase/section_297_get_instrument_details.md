# Get instrument details
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/instruments/get-instrument-details

GET /api/v1/instruments/{instrument}
Retrieves market information for a specific instrument.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    InstrumentsService instrumentsService = IntxServiceFactory.createInstrumentsService(client);
    GetInstrumentRequest request = new GetInstrumentRequest.Builder()
        .instrumentId("BTC-PERP")
        .build();
    GetInstrumentResponse response = instrumentsService.getInstrument(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var instrumentsService = new InstrumentsService(client);
    var request = new GetInstrumentRequest(
        InstrumentId: "BTC-PERP",
    );
    var response = instrumentsService.GetInstrument(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    instrumentsSvc := instruments.NewInstrumentsService(client)
    request := &instruments.GetInstrumentRequest{
        InstrumentId: "BTC-PERP",
    }
    response, err := instrumentsSvc.GetInstrument(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetInstrumentDetailsRequest(
        instrument_id="BTC-PERP",
    )
    response = client.get_instrument_details(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const instrumentsService = new InstrumentsService(client);

    instrumentsService.getInstrument({
        instrumentId: 'ETH-PERP',
    }).then(async (response) => {
        console.log('Instrument: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-instrument-details --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

