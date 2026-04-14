# List position offsets
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/position-offsets/list-position-offsets

GET /api/v1/position-offsets
Returns all active position offsets

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const positionOffsetsService = new PositionOffsetsService(client);

    positionOffsetsService.listPositionOffsets().then(async (response) => {
        console.log('Position Offsets: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

