# Get daily trading volumes
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/instruments/get-daily-trading-volume

GET /api/v1/instruments/volumes/daily
Retrieves the trading volumes for each instrument separated by day.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    InstrumentsService instrumentsService = IntxServiceFactory.createInstrumentsService(client);
    GetDailyTradingVolumesRequest request = new GetDailyTradingVolumesRequest.Builder()
        .instruments("BTC-PERP")
        .build();
    GetDailyTradingVolumesResponse response = instrumentsService.getDailyTradingVolumes(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var instrumentsService = new InstrumentsService(client);
    var request = new GetDailyTradingVolumesRequest(
        instruments: "BTC-PERP"
    );
    var response = instrumentsService.GetDailyTradingVolumes(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetDailyTradingVolumesRequest(
        instruments="BTC-PERP"
    )
    response = client.get_instrument_volumes_daily(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const instrumentsService = new InstrumentsService(client);

    instrumentsService.getDailyTradingVolume({
        instrument: 'BTC-PERP',
    }).then(async (response) => {
        console.log('Daily Trading Volume: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

