# Enable/Disable portfolio auto margin mode
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/enable-and-disable-portfolio

POST /api/v1/portfolios/{portfolio}/auto-margin-enabled
Enable or disable the auto margin feature, which lets the portfolio automatically post margin amounts required to exceed the high leverage position restrictions.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    EnableDisableAutoMarginRequest request = new EnableDisableAutoMarginRequest.Builder()
        .enabled(True)
        .build();
    EnableDisableAutoMarginResponse response = portfoliosService.enableDisableAutoMargin(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new EnableDisableAutoMarginRequest(
        Enabled: true,
    );
    var response = portfoliosService.EnableDisableAutoMargin(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = EnableDisableAutoMarginRequest(
        enabled=True,
    )
    response = client.enable_disable_auto_margin(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.updateAutoMargin({
        portfolio: 'PORTFOLIO_ID_HERE',
        enabled: true,
    }).then(async (response) => {
        console.log('Auto Margin Updated: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>
</Tabs>

