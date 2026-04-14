# Get index candles
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/index/get-index-candles

GET /api/v1/index/{index}/candles
Retrieves the historical daily index prices in time descending order. The daily values are represented as aggregated entries for the day in typical OHLC format.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const indexService = new IndexService(client);

    indexService.getIndexCandles({
        index: 'COIN50',
        granularity: 'ONE_DAY',
        start: '2024-01-01T00:00:00Z',
    }).then(async (response) => {
        console.log('Index Candles: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

