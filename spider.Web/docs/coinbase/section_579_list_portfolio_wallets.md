# List Portfolio Wallets
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/wallets/list-portfolio-wallets

GET /v1/portfolios/{portfolio_id}/wallets
List all wallets associated with a given portfolio.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    WalletsService walletsService = PrimeServiceFactory.createWalletsService(client);

    ListWalletsRequest request = new ListWalletsRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .type(WalletType.VAULT)
        .build();

    ListWalletsResponse response = walletsService.listWallets(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var walletsService = new WalletsService(client);

    var request = new ListWalletsRequest("PORTFOLIO_ID_HERE")
    {
        Type = WalletType.VAULT,
    }

    var response = walletsService.ListWallets(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    walletsService := users.NewWalletsService(client)

    request := &users.ListWalletsRequest{
        PortfolioId: "PORTFOLIO_ID_HERE",
        Type: "VAULT",
    }

    response, err := walletsService.ListWallets(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListWalletsRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        type="VAULT",
    )

    response = prime_client.list_wallets(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-wallets --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const walletsService = new WalletsService(client);

    walletsService.listWallets({
        portfolioId: 'PORTFOLIO_ID_HERE',
        type: WalletType.VAULT,
    }).then(async (response) => {
        console.log('Wallets: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

