# View max loan availability
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/view-max-loan

GET /api/v1/portfolios/{portfolio}/loans/{asset}/availability
View the maximum amount of loan that could be acquired now

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const positionOffsetsService = new PositionOffsetsService(client);

    positionOffsetsService.getAssetLoanAvailability({
        portfolio: 'PORTFOLIO_ID_HERE',
        asset: 'ETH',
    }).then(async (response) => {
        console.log('Available Asset Loan: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

