# List Portfolio Fills
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/list-portfolio-fills

GET /v1/portfolios/{portfolio_id}/fills
Retrieve fills on a given portfolio. This endpoint requires a start_date, and returns a payload with a default limit of 100 if not specified by the user. The maximum allowed limit is 3000.

<Tip>
  **Prime CLI**

  Use the [Prime CLI](https://github.com/coinbase-samples/prime-cli) to test this endpoint by following the [quick start](/prime/introduction/quickstart) guide and running this command:

  ```bash lines wrap theme={null}
  primectl get-portfolio-fills --help
  ```
</Tip>

<Tabs>
  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-portfolio-fills --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const ordersService = new OrdersService(client);

    ordersService.listPortfolioFills({
        portfolioId: 'PORTFOLIO_ID_HERE',
        orderId: 'ORDER_ID_HERE',
    }).then(async (response) => {
        console.log('Fills: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

