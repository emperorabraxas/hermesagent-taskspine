# List assets
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/assets/list-assets

GET /api/v1/assets
Returns a list of all supported assets.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    AssetsService assetsService = IntxServiceFactory.createAssetsService(client);
    ListAssetsRequest request = new ListAssetsRequest.Builder().build();
    ListAssetsResponse response = assetsService.listAssets(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var assetsService = new AssetsService(client);
    var request = new ListAssetsRequest();
    var response = assetsService.ListAssets(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    assetsSvc := assets.NewAssetsService(client)
    request := &assets.ListAssetsRequest{}
    response, err := assetsSvc.ListAssets(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = ListAssetsRequest()
    response = client.list_assets(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const assetsService = new AssetsService(client);

    assetsService.listAssets().then(async (response) => {
        console.log('Assets: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl list-assets --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

