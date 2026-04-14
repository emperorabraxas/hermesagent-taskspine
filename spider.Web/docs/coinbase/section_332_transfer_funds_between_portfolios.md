# Transfer funds between portfolios
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/transfer-funds

POST /api/v1/portfolios/transfer
Transfer assets from one portfolio to another.

## API Key Permissions

This endpoint requires an API key with `transfer` permission.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    TransferFundsRequest request = new TransferFundsRequest.Builder()
        .from("portfolio_id_1")
        .to("portfolio_id_2")
        .asset("BTC")
        .amount("1")
        .build();
    TransferFundsResponse response = portfoliosService.transferFunds(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new TransferFundsRequest(
        From: "portfolio_id_1",
        To: "portfolio_id_2",
        Asset: "BTC",
        Amount: "1",
    );
    var response = portfoliosService.TransferFunds(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    ordersSvc := orders.NewOrdersService(client)
    request := &portfolios.CreatePortfolioTransferRequest{
        From: "portfolio_id_1",
        To: "portfolio_id_2",
        Asset: "BTC",
        Amount: "1",
    }
    response, err := portfoliosSvc.CreatePortfolioTransfer(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = TransferFundsRequest(
        from="portfolio_id_1",
        to="portfolio_id_2",
        asset="BTC",
        amount="1",
    )
    response = client.transfer_funds(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.createTransferFunds({
        from: 'portfolio_id_1',
        to: 'portfolio_id_2',
        asset: 'ETH',
        amount: '1',
    }).then(async (response) => {
        console.log('Transfer Created: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl create-portfolio-transfer --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

