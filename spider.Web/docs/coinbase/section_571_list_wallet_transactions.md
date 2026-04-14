# List Wallet Transactions
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/transactions/list-wallet-transactions

GET /v1/portfolios/{portfolio_id}/wallets/{wallet_id}/transactions
Retrieve transactions for a given wallet.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransactionsService transactionsService = PrimeServiceFactory.createTransactionsService(client);

    ListWalletTransactionsRequest request = new ListWalletTransactionsRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .build();

    ListWalletTransactionsResponse response = transactionsService.listWalletTransactions(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    TransactionsService transactionsService = PrimeServiceFactory.createTransactionsService(client);

    ListWalletTransactionsRequest request = new ListWalletTransactionsRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .build();

    ListWalletTransactionsResponse response = transactionsService.listWalletTransactions(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    transactionsService := transactions.NewTransactionsService(client)

    request := &transactions.ListWalletTransactionsRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        WalletId: "WALLET_ID_HERE",
    }

    response, err := transactionsService.ListWalletTransactions(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListWalletTransactionsRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
    )

    response = prime_client.list_wallet_transactions(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-wallet-transactions --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const transactionsService = new TransactionsService(client);

    transactionsService.listWalletTransactions({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE'
    }).then(async (response) => {
        console.log('Transactions: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

