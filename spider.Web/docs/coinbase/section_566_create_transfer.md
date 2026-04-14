# Create Transfer
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/transactions/create-transfer

POST /v1/portfolios/{portfolio_id}/wallets/{wallet_id}/transfers
Create a wallet transfer.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransactionsService transactionsService = PrimeServiceFactory.createTransactionsService(client);

    CreateTransferRequest request = new CreateTransferRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .amount("0.001")
        .destination("DESTINATION_WALLET_UUID")
        .idempotencyKey(UUID.randomUUID().toString())
        .currencySymbol("ETH")
        .build();

    CreateTransferResponse response = transactionsService.createTransfer(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var transactionsService = new TransactionsService(client);

    var request = new CreateTransferRequest("PORTFOLIO_ID_HERE", "WALLET_ID_HERE")
    {
        Amount = "0.001",
        Destination = "DESTINATION_WALLET_UUID",
        IdempotencyKey = Guid.NewGuid().ToString(),
        CurrencySymbol = "ETH",
    };

    var response = transactionsService.CreateTransfer(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    transactionsService := transactions.NewTransactionsService(client)

    request := &transactions.CreateWalletTransferRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        WalletId: "WALLET_ID_HERE",
        Amount: "0.001",
        Destination: "DESTINATION_WALLET_UUID",
        IdempotencyKey: uuid.New().String(),
        CurrencySymbol: "ETH",
    }

    response, err := transactionsService.CreateWalletTransfer(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = CreateTransferRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
        amount = '0.001',
        destination = 'DESTINATION_WALLET_UUID',
        idempotency_key = str(uuid.uuid4()),
        currency_symbol = 'ETH',
    )

    response = prime_client.create_transfer(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl create-transfer --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const transactionsService = new TransactionsService(client);

    transactionsService.createTransfer({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE',
        amount: "0.001",
        destination: "DESTINATION_WALLET_UUID",
        idempotencyKey: uuidv4(),
        currencySymbol: "ETH",

    }).then(async (response) => {
        console.log('Transfer: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

