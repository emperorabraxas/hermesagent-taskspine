# Get Wallet by Wallet ID
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/wallets/get-wallet-by-wallet-id

GET /v1/portfolios/{portfolio_id}/wallets/{wallet_id}
Retrieve a specific wallet by Wallet ID.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    WalletsService walletsService = PrimeServiceFactory.createWalletsService(client);

    GetWalletByIdRequest request = new GetWalletByIdRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .build();

    GetWalletByIdResponse response = walletsService.getWalletById(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var walletsService = new WalletsService(client);

    var request = new GetWalletByIdRequest("PORTFOLIO_ID_HERE", "WALLET_ID_HERE");

    var response = walletsService.GetWalletById(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    walletsService := users.NewWalletsService(client)

    request := &users.GetWalletRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        Id: "WALLET_ID_HERE",
    }

    response, err := walletsService.GetWallet(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetWalletRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
    )

    response = prime_client.get_wallet(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-wallet --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const walletsService = new WalletsService(client);

    walletsService.getWallets({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE'
    }).then(async (response) => {
        console.log('Wallet: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

