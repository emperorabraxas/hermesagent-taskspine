# Transfer positions between portfolios
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/transfer-positions

POST /api/v1/portfolios/transfer-position
Transfer an existing position from one portfolio to another. The position transfer must fulfill the same portfolio-level margin requirements as submitting a new order on the opposite side for the sender's portfolio and a new order on the same side  for the recipient's portfolio. Additionally, organization-level requirements must be satisfied when evaluating the outcome of the position transfer.

## API Key Permissions

This endpoint requires an API key with `trade` permission.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    TransferPositionsRequest request = new TransferPositionsRequest.Builder()
        .from("portfolio_id_1")
        .to("portfolio_id_2")
        .instrument("BTC-PERP")
        .amount("1")
        .build();
    TransferPositionsResponse response = portfoliosService.transferPositions(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new TransferPositionsRequest(
        From: "portfolio_id_1",
        To: "portfolio_id_2",
        Instrument: "BTC-PERP",
        Amount: "1",
    );
    var response = portfoliosService.TransferPositions(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = TransferPositionRequest(
        from="portfolio_id_1",
        to="portfolio_id_2",
        instrument="BTC-PERP",
        amount="1",
    )
    response = client.transfer_positions(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.createTransferPosition({
        from: 'portfolio_id_1',
        to: 'portfolio_id_2',
        instrument: 'ETH-PERP',
        amount: '1',
    }).then(async (response) => {
        console.log('Transfer Created: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

