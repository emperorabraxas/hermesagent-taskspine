# Get index composition history
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/index/get-index-composition-history

GET  /api/v1/index/{index}/composition-history
Retrieves a history of index composition records in a descending time order. The results are an array of index composition data recorded at different "timestamps".

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const indexService = new IndexService(client);

    indexService.getIndexCompositionHistory({
        index: 'COIN50',
    }).then(async (response) => {
        console.log('Index Composition History: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

