# Get Wallet Balance
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/balances/get-wallet-balance

GET /v1/portfolios/{portfolio_id}/wallets/{wallet_id}/balance
Query balance for a specific wallet.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    BalancesService balancesService = PrimeServiceFactory.createBalancesService(client);

    GetWalletBalanceRequest request = new GetWalletBalanceRequest.Builder()
        .portfolioId("PORTFOLIO_ID_HERE")
        .walletId("WALLET_ID_HERE")
        .build();

    GetWalletBalanceResponse response = balancesService.getWalletBalance(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var balancesService = new BalancesService(client);

    var request = new GetWalletBalanceRequest("PORTFOLIO_ID_HERE", "WALLET_ID_HERE");
    var response = balancesService.GetWalletBalance(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    balancesService := balances.NewBalancesService(client)

    request := &balances.GetWalletBalance{
        PortfolioId: "PORTFOLIO_ID_HERE",
        WalletId: "WALLET_ID_HERE",
    }

    response, err := balancesService.GetWalletBalance(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetWalletBalanceRequest(
            portfolio_id="PORTFOLIO_ID_HERE",
            wallet_id="WALLET_ID_HERE",
    )

    response = prime_client.get_wallet_balance(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-wallet-balance --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const balancesService = new BalancesService(client);

    balancesService.getWalletBalance({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE'
    }).then(async (response) => {
        console.log('Balances: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

