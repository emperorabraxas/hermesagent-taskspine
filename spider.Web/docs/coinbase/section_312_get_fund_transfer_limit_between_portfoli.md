# Get fund transfer limit between portfolios
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-fund-transfer-limit

GET /api/v1/portfolios/transfer/{portfolio}/{asset}/transfer-limit
Get fund transfer limit between portfolios of the same beneficial owner

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getFundTransferLimit({
        portfolio: 'PORTFOLIO_ID_HERE',
        asset: 'ETH',
    }).then(async (response) => {
        console.log('Fund Transfer Limit: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

