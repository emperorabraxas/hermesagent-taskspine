# Get Transaction by Transaction ID
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/transactions/get-transaction-by-transaction-id

GET /v1/portfolios/{portfolio_id}/transactions/{transaction_id}
Retrieve a specific transaction by its transaction ID.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransactionsService transactionsService = PrimeServiceFactory.createTransactionsService(client);

    GetTransactionByTransactionIdRequest request = new GetTransactionByTransactionIdRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .transactionId("TRANSACTION_ID_HERE")
        .build();

    GetTransactionByTransactionIdResponse response = transactionsService.getTransactionByTransactionId(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var transactionsService = new TransactionsService(client);

    var request = new GetTransactionByTransactionIdRequest("PORTFOLIO_ID_HERE", "TRANSACTION_ID_HERE");

    var response = transactionsService.GetPortfolioById(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    transactionsService := transactions.NewTransactionsService(client)

    request := &transactions.GetPortfolio{
        PortfolioId: "PORTFOLIO_ID_HERE",
        TransactionId: "TRANSACTION_ID_HERE",
    }

    response, err := transactionsService.GetTransactions(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetTransactionRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        transaction_id="TRANSACTION_ID_HERE",
    )

    response = prime_client.get_transaction(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-transaction --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const transactionsService = new TransactionsService(client);

    transactionsService.getTransaction({
        portfolioId: 'PORTFOLIO_ID_HERE',
        transactionId: 'TRANSACTION_ID_HERE',
    }).then(async (response) => {
        console.log('Transaction: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

