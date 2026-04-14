# Get index composition
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/index/get-index-composition

GET  /api/v1/index/{index}/composition
Retrieves the latest index composition (metadata) with an ordered set of constituents.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const indexService = new IndexService(client);

    indexService.getIndexComposition({
        index: 'COIN50',
    }).then(async (response) => {
        console.log('Index Composition: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

