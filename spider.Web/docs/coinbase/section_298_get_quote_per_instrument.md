# Get quote per instrument
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/instruments/get-quote-per-instrument

GET /api/v1/instruments/{instrument}/quote
Retrieves the current quote for a specific instrument.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    InstrumentsService instrumentsService = IntxServiceFactory.createInstrumentsService(client);
    GetInstrumentQuoteRequest request = new GetInstrumentQuoteRequest.Builder()
        .instrumentId("BTC-PERP")
        .build();
    GetInstrumentQuoteResponse response = instrumentsService.getInstrumentQuote(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var instrumentsService = new InstrumentsService(client);
    var request = new GetInstrumentQuoteRequest(
        InstrumentId: "BTC-PERP",
    );
    var response = instrumentsService.GetInstrumentQuote(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    instrumentsSvc := instruments.NewInstrumentsService(client)
    request := &instruments.GetInstrumentQuoteRequest{
        InstrumentId: "BTC-PERP",
    }
    response, err := instrumentsSvc.GetInstrumentQuote(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetQuotePerInstrumentRequest(
        instrument_id="BTC-PERP",
    )
    response = client.get_quote_per_instrument(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const instrumentsService = new InstrumentsService(client);

    instrumentsService.getQuote({
        instrument: 'ETH-PERP',
    }).then(async (response) => {
        console.log('Instrument Quote: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-quote-per-instrument --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

