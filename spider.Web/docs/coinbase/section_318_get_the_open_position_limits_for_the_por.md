# Get the open position limits for the portfolio instrument
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-the-open-position-limits

GET /api/v1/portfolios/{portfolio}/position-limits/positions/{instrument}
Retrieves the position limits for a given portfolio and symbol.

<Tabs>
  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getInstrumentPositionLimit({
        portfolio: 'PORTFOLIO_ID_HERE',
        instrument: 'ETH-PERP',
    }).then(async (response) => {
        console.log('Instrument Position Limits: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

