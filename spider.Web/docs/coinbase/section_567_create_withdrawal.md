# Create Withdrawal
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/transactions/create-withdrawal

POST /v1/portfolios/{portfolio_id}/wallets/{wallet_id}/withdrawals
Create a withdrawal.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    TransactionsService transactionsService = PrimeServiceFactory.createTransactionsService(client);

    CreateWithdrawalRequest request = new CreateWithdrawalRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .amount("0.001")
        .destinationType(DestinationType.DESTINATION_BLOCKCHAIN)
        .idempotencyKey(UUID.randomUUID().toString())
        .currencySymbol("ETH")
        .blockchainAddress(new BlockchainAddress.Builder()
            .address("DESTINATION_WALLET_ADDRESS")
            .build())
        .build();

    CreateWithdrawalResponse response = transactionsService.createWithdrawal(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var transactionsService = new TransactionsService(client);

    var request = new CreateWithdrawalRequest("PORTFOLIO_ID_HERE", "WALLET_ID_HERE")
    {
        Amount = "0.001",
        DestinationType = DestinationType.DESTINATION_BLOCKCHAIN,
        IdempotencyKey = Guid.NewGuid().ToString(),
        CurrencySymbol = "ETH",
        BlockchainAddress = new BlockchainAddress
        {
            Address = "DESTINATION_WALLET_ADDRESS",
        },
    };

    var response = transactionsService.CreateWithdrawal(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    transactionsService := transactions.NewTransactionsService(client)

    request := &transactions.CreateWalletWithdrawalRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        WalletId: "WALLET_ID_HERE",
        Amount: "0.001",
        DestinationType: "DESTINATION_BLOCKCHAIN",
        IdempotencyKey: uuid.New().String(),
        Symbol: "ETH",
        BlockchainAddress: &transactions.BlockchainAddress{
            Address: "DESTINATION_WALLET_ADDRESS",
        },
    }

    response, err := transactionsService.CreateWalletWithdrawal(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = CreateWithdrawalRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
        amount = '0.001',
        destination_type = 'DESTINATION_BLOCKCHAIN',
        idempotency_key = str(uuid.uuid4()),
        currency_symbol = 'ETH',
        blockchain_address = BlockchainAddress(
            address='DESTINATION_WALLET_ADDRESS',
        ),
    )

    response = prime_client.create_withdrawal(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl create-withdrawal --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const transactionsService = new TransactionsService(client);

    transactionsService.createWithdrawal({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE',
        amount: "0.001",
        idempotencyKey: uuidv4(),
        currencySymbol: "ETH",
        destinationType: DestinationType.DestinationBlockchain,
        blockchainAddress: {
            address: 'DESTINATION_WALLET_ADDRESS',
        }
    }).then(async (response) => {
        console.log('Withdrawal: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

