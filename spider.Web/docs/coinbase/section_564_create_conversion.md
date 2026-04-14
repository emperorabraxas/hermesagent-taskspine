# Create Conversion
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/transactions/create-conversion

POST /v1/portfolios/{portfolio_id}/wallets/{wallet_id}/conversion
Perform a conversion between 2 assets.

<Info>
  **Supported Swaps**

  This endpoint supports the following conversions: USD \<> USDC and USD \<> PYUSD.

  For more assistance on how to create and track conversions, visit the [stablecoins](/prime/concepts/stablecoins) concepts page.
</Info>

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransactionsService transactionsService = PrimeServiceFactory.createTransactionsService(client);

    CreateConversionRequest request = new CreateConversionRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .amount("1")
        .destination("DESTINATION_WALLET_UUID")
        .idempotencyKey(UUID.randomUUID().toString())
        .sourceSymbol("USD")
        .destinationSymbol("USDC")
        .build();

    CreateConversionResponse response = transactionsService.createConversion(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var transactionsService = new TransactionsService(client);

    var request = new CreateConversionRequest("PORTFOLIO_ID_HERE", "WALLET_ID_HERE")
    {
        Amount = "1",
        Destination = "DESTINATION_WALLET_UUID",
        IdempotencyKey = Guid.NewGuid().ToString(),
        SourceSymbol = "USD",
        DestinationSymbol = "USDC",
    };

    var response = transactionsService.CreateConversion(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    transactionsService := transactions.NewTransactionsService(client)

    request := &transactions.CreateConversionRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        WalletId: "WALLET_ID_HERE",
        Amount: "1",
        Destination: "DESTINATION_WALLET_UUID",
        IdempotencyKey: uuid.New().String(),
        SourceSymbol: "USD",
        DestinationSymbol: "USDC",
    }

    response, err := transactionsService.CreateConversion(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = CreateConversionRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
        amount = '1',
        destination = 'DESTINATION_WALLET_UUID',
        idempotency_key = str(uuid.uuid4()),
        source_symbol = 'USD',
        destination_symbol = 'USDC',
    )

    response = prime_client.create_conversion(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl create-conversion --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const transactionsService = new TransactionsService(client);

    transactionsService.createConversion({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE',
        amount: "1",
        destination: "DESTINATION_WALLET_UUID",
        idempotencyKey: uuidv4(),
        sourceSymbol: "USD",
        destinationSymbol: "USDC",

    }).then(async (response) => {
        console.log('Conversion: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

