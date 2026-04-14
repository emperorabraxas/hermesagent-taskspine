# Get Wallet Deposit Instructions
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/wallets/get-wallet-deposit-instructions

GET /v1/portfolios/{portfolio_id}/wallets/{wallet_id}/deposit_instructions
Retrieve a specific wallet's deposit instructions.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    WalletsService walletsService = PrimeServiceFactory.createWalletsService(client);

    GetWalletDepositInstructionsRequest request = new GetWalletDepositInstructionsRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .depositType(DepositType.CRYPTO)
        .build();

    GetWalletDepositInstructionsResponse response = walletsService.getWalletDepositInstructions(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var walletsService = new WalletsService(client);

    var request = new GetWalletDepositInstructionsRequest("PORTFOLIO_ID_HERE", "WALLET_ID_HERE")
    {
        DepositType = DepositType.CRYPTO,
    };

    var response = walletsService.GetWalletDepositInstructions(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    walletsService := users.NewWalletsService(client)

    request := &users.GetWalletDepositInstructionsRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        Id: "WALLET_ID_HERE",
        DepositType: "CRYPTO",
    }

    response, err := walletsService.GetWalletDepositInstructions(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetWalletDepositInstructionsDepositInstructionsRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
        deposit_type="CRYPTO",
    )

    response = prime_client.get_wallet_deposit_instructions(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-wallet-deposit-instructions --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const walletsService = new WalletsService(client);

    walletsService.getWalletDepositInstructions({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE',
    }).then(async (response) => {
        console.log('Deposit Instructions: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

