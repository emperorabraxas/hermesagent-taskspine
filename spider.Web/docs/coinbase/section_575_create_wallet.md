# Create Wallet
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/wallets/create-wallet

POST  /v1/portfolios/{portfolio_id}/wallets
Create a wallet. Note: The first ONCHAIN wallet for each network family must be created through the Prime UI.

<Info>
  **Supported Types**

  Currently, this endpoint can be used only to create vault wallets and onchain wallets that do not require key generation. The first EVM and first Solana onchain wallet in a portfolio must be created prior to creating subsequent EVM or Solana wallets in a portfolio via API.
</Info>

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    WalletsService walletsService = PrimeServiceFactory.createWalletsService(client);

    CreateWalletRequest request = new CreateWalletRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .type(WalletType.VAULT)
        .name("PRIME_API_EXAMPLE")
        .symbol("ETH")
        .build();

    CreateWalletResponse response = walletsService.createWallet(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var walletsService = new WalletsService(client);

    var request = new CreateWalletRequest("PORTFOLIO_ID_HERE")
    {
        Type = WalletType.VAULT,
        Name = "PRIME_API_EXAMPLE",
        Symbol = "ETH",
    }

    var response = walletsService.CreateWallet(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    walletsService := users.NewWalletsService(client)

    request := &users.CreateWalletRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        Type: "VAULT",
        Name: "PRIME_API_EXAMPLE",
        Symbol: "ETH",
    }

    response, err := walletsService.CreateWallet(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = CreateWalletRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        name="PRIME_API_EXAMPLE",
        symbol="ETH",
        wallet_type="VAULT",
    )

    response = prime_client.create_wallet(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl create-wallet --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const walletsService = new WalletsService(client);

    walletsService.getWalletDepositInstructions({
        portfolioId: 'PORTFOLIO_ID_HERE',
        type: WalletType.VAULT,
        name: "PRIME_API_EXAMPLE",
        symbol: "ETH",
    }).then(async (response) => {
        console.log('Wallet: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

