# Get historical funding rates
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/instruments/get-historical-funding-rate

GET /api/v1/instruments/{instrument}/funding
Retrieves the historical funding rates for a specific instrument.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    InstrumentsService instrumentsService = IntxServiceFactory.createInstrumentsService(client);
    GetHistoricalFundingRatesRequest request = new GetHistoricalFundingRatesRequest.Builder()
        .instrumentId("BTC-PERP")
        .build();
    GetHistoricalFundingRatesResponse response = instrumentsService.getHistoricalFundingRates(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var instrumentsService = new InstrumentsService(client);
    var request = new GetHistoricalFundingRatesRequest(
        InstrumentId: "BTC-PERP",
    );
    var response = instrumentsService.GetHistoricalFundingRates(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    instrumentsSvc := instruments.NewInstrumentsService(client)
    request := &instruments.GetHistoricalFundingRequest{
        InstrumentId: "BTC-PERP",
    }
    response, err := instrumentsSvc.GetHistoricalFunding(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetHistoricalFundingRatesRequest(
        instrument_id="BTC-PERP",
    )
    response = client.get_historical_funding_rates(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const instrumentsService = new InstrumentsService(client);

    instrumentsService.getHistoricalFundingRates({
        instrument: 'ETH-PERP',
    }).then(async (response) => {
        console.log('Historical Funding Rates: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-historical-funding-rates --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

