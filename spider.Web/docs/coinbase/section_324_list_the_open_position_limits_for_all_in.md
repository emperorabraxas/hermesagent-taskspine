# List the open position limits for all instruments
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/list-open-position-limit

GET /api/v1/portfolios/{portfolio}/position-limits/positions
Retrieves position limits for all positions a given portfolio currently has or has opened in the past.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getInstrumentPositionLimit({
        portfolio: 'PORTFOLIO_ID_HERE',
        instrument: 'ETH',
    }).then(async (response) => {
        console.log('Position Limits: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

