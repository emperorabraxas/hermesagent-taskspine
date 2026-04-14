# Get balance for portfolio/asset
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-balance-for-assests

GET /api/v1/portfolios/{portfolio}/balances/{asset}
Retrieves the balance for a given portfolio and asset.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    GetBalanceForPortfolioAssetRequest request = new GetBalanceForPortfolioAssetRequest.Builder()
        .portfolio("portfolio_id")
        .asset("BTC")
        .build();
    GetBalanceForPortfolioAssetResponse response = portfoliosService.getBalanceForPortfolioAsset(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new GetBalanceForPortfolioAssetRequest(
        Portfolio: "portfolio_id",
        Asset: "BTC",
    );
    var response = portfoliosService.GetBalanceForPortfolioAsset(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.GetAssetBalanceRequest{
        Portfolio: "portfolio_id",
        Asset: "BTC",
    }
    response, err := portfoliosSvc.GetAssetBalance(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetBalanceForPortfolioAssetRequest(
        portfolio="portfolio_id",
        asset="BTC",
    )
    response = client.get_balance_for_portfolio_asset(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getAssetBalance({
        portfolio: 'PORTFOLIO_ID_HERE',
        asset: 'ETH',
    }).then(async (response) => {
        console.log('Portfolio Asset Balance: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-balance-for-asset --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

