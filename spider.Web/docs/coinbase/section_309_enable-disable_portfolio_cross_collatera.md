# Enable/Disable portfolio cross collateral
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/enable-and-disable-cross

POST  /api/v1/portfolios/{portfolio}/cross-collateral-enabled
Enable or disable the cross collateral feature for the portfolio, which allows the portfolio to use non-USDC assets as collateral for margin trading.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    EnableDisableCrossCollateralRequest request = new EnableDisableCrossCollateralRequest.Builder()
        .enabled(True)
        .build();
    EnableDisableCrossCollateralResponse response = portfoliosService.enableDisableCrossCollateral(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new EnableDisableCrossCollateralRequest(
        Enabled: true,
    );
    var response = portfoliosService.EnableDisableCrossCollateral(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = EnableDisableCrossCollateralRequest   (
        enabled=True,
    )
    response = client.enable_disable_cross_collateral(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.updateCrossCollateral({
        portfolio: 'PORTFOLIO_ID_HERE',
        enabled: true,
    }).then(async (response) => {
        console.log('Cross Collateral Updated: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

