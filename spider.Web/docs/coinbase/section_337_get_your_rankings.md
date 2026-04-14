# Get your rankings
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/rankings/get-your-rankings

GET /api/v1/rankings/statistics
Retrieve your volume rankings for maker, taker, and total volume.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const rankingsService = new RankingsService(client);

    rankingsService.getRankings().then(async (response) => {
        console.log('Volume Rankings: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

