# Get asset details
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/assets/get-asset-details

GET /api/v1/assets/{asset}
Retrieves information for a specific asset.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    AssetsService assetsService = IntxServiceFactory.createAssetsService(client);
    GetAssetRequest request = new GetAssetRequest.Builder()
        .assetId("BTC")
        .build();
    GetAssetResponse response = assetsService.getAsset(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var assetsService = new AssetsService(client);
    var request = new GetAssetRequest(
        AssetId: "BTC",
    );
    var response = assetsService.GetAsset(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    assetsSvc := assets.NewAssetsService(client)
    request := &assets.GetAssetRequest{
        AssetId: "BTC",
    }
    response, err := assetsSvc.GetAsset(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetAssetRequest(
        asset_id="BTC",
    )
    response = client.get_asset(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const assetsService = new AssetsService(client);

    assetsService.getAsset({
        asset: 'ETH',
    }).then(async (response) => {
        console.log('Asset: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-asset --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

