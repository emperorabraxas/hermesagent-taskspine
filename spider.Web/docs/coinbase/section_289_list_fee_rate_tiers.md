# List fee rate tiers
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/fee-rates/list-fee-rate-tiers

GET /api/v1/fee-rate-tiers
Return all the fee rate tiers.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    FeeRatesService feeRatesService = IntxServiceFactory.createFeeRatesService(client);
    GetFeeRateTiersResponse response = feeRatesService.getFeeRateTiers();
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var feeRatesService = new FeeRatesService(client);
    var response = feeRatesService.GetFeeRateTiers();
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListFeeRateTiersRequest()
    response = client.list_fee_rate_tiers(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const feeRatesService = new FeeRatesService(client);

    feeRatesService.listFeeRateTiers().then(async (response) => {
        console.log('Fee Rate Tiers: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

