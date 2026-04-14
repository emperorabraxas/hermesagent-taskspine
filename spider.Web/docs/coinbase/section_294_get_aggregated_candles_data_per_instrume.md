# Get aggregated candles data per instrument
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/instruments/get-aggegated-candles

GET /api/v1/instruments/{instrument}/candles
Retrieves a list of aggregated candles data for a given instrument, granularity and time range

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    InstrumentsService instrumentsService = IntxServiceFactory.createInstrumentsService(client);
    GetAggregatedCandlesRequest request = new GetAggregatedCandlesRequest.Builder()
        .instrumentId("BTC-PERP")
        .granularity("ONE_DAY")
        .start("2024-01-01T00:00:00Z")
        .build();
    GetAggregatedCandlesResponse response = instrumentsService.getAggregatedCandles(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var instrumentsService = new InstrumentsService(client);
    var request = new GetAggregatedCandlesRequest(
        InstrumentId: "BTC-PERP",
        Granularity: "ONE_DAY",
        Start: "2024-01-01T00:00:00Z",
    );
    var response = instrumentsService.GetAggregatedCandles(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetAggregatedCandlesRequest(
        instrument_id="BTC-PERP",
        granularity="ONE_DAY",
        start="2024-01-01T00:00:00Z",
    )
    response = client.get_aggregated_candles(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const instrumentsService = new InstrumentsService(client);

    instrumentsService.getAggregatedCandles({
        instrumentId: 'BTC-PERP',
        granularity: 'ONE_DAY',
        start: '2024-01-01T00:00:00Z',
    }).then(async (response) => {
        console.log('Aggregated Candles: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

