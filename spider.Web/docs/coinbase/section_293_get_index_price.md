# Get index price
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/index/get-index-price

GET /api/v1/index/{index}/price
Retrieves the latest index price

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const indexService = new IndexService(client);

    indexService.getIndexPrice({
        index: 'COIN50',
    }).then(async (response) => {
        console.log('Index Price: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

