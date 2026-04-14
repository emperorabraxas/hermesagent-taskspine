# Withdraw to counterparty Id
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/transfers/withdraw-to-counterparty-id

POST /api/v1/transfers/withdraw/counterparty

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransfersService transfersService = IntxServiceFactory.createTransfersService(client);
    WithdrawToCounterpartyIdRequest request = new WithdrawToCounterpartyIdRequest.Builder()
        .portfolio("portfolio_id")
        .counterpartyId("counterparty_id")
        .asset("BTC")
        .amount("1")
        .build();
    WithdrawToCounterpartyIdResponse response = transfersService.withdrawToCounterpartyId(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var transfersService = new TransfersService(client);
    var request = new WithdrawToCounterpartyIdRequest(
        Portfolio: "portfolio_id",
        CounterpartyId: "counterparty_id",
        Asset: "BTC",
        Amount: "1",
    );
    var response = transfersService.WithdrawToCounterpartyId(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    transfersSvc := transfers.NewTransfersService(client)
    request := &transfers.CreateWithdrawalToCounterpartyIdRequest{
        Portfolio: "portfolio_id",
        CounterpartyId: "counterparty_id",
        Asset: "BTC",
        Amount: "1",
    }
    response, err := transfersSvc.CreateWithdrawalToCounterpartyId(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = WithdrawToCounterpartyIdRequest(
        portfolio="portfolio_id",
        counterparty_id="counterparty_id",
        asset="BTC",
        amount="1",
    )
    response = client.withdraw_to_counterparty_id(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const transfersService = new TransfersService(client);

    transfersService.withdrawToCounterparty({
        portfolio: 'PORTFOLIO_ID_HERE',
        counterpartyId: 'COUNTERPARTY_ID_HERE',
        asset: 'BTC',
        amount: "1",
        nonce: 12345
    }).then(async (response) => {
        console.log('Withdrawal created: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl create-withdrawal-to-counterparty-id --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

