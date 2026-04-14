# List Assets
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/assets/list-assets

GET /v1/entities/{entity_id}/assets
List all assets available for a given entity.

<Info>
  **Entity ID**

  To retrieve your entity\_id, use [List Portfolios](/api-reference/prime-api/rest-api/portfolios/list-portfolios).
</Info>

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-assets --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const assetsService = new AssetsService(client);

    assetsService.listAssets({
        entityId: 'ENTITY_ID_HERE'
    }).then(async (response) => {
        console.log('Assets: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

