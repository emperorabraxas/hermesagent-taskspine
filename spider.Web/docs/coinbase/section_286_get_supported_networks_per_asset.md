# Get supported networks per asset
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/assets/get-supported-networks

GET /api/v1/assets/{asset}/networks
Returns a list of supported networks and network information for a specific asset.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    AssetsService assetsService = IntxServiceFactory.createAssetsService(client);
    GetSupportedNetworksRequest request = new GetSupportedNetworksRequest.Builder()
        .asset("BTC")
        .build();
    GetSupportedNetworksResponse response = assetsService.getSupportedNetworks(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var assetsService = new AssetsService(client);
    var request = new GetSupportedNetworksRequest(
        Asset: "BTC",
    );
    var response = assetsService.GetSupportedNetworks(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    assetsSvc := assets.NewAssetsService(client)
    request := &assets.GetSupportedNetworksRequest{
        Asset: "BTC",
    }
    response, err := assetsSvc.GetSupportedNetworks(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetSupportedNetworksRequest(
        asset="BTC",
    )
    response = client.get_supported_networks(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const assetsService = new AssetsService(client);

    assetsService.getSupportedNetworks({
        asset: 'ETH',
    }).then(async (response) => {
        console.log('Supported Networks: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-supported-networks --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

