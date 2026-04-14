# Acquire/repay loan
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/acquire-and-repay-loan

POST /api/v1/portfolios/{portfolio}/loans/{asset}
Acquire or repay loan for a given portfolio and asset.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const positionOffsetsService = new PositionOffsetsService(client);

    positionOffsetsService.acquireOrRepayLoan({
        portfolio: 'PORTFOLIO_ID_HERE',
        asset: 'ETH',
        action: LoanUpdateAction.ACQUIRE,
        amount: '1',
    }).then(async (response) => {
        console.log('Active Loan: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

