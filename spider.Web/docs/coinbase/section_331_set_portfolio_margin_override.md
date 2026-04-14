# Set portfolio margin override
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/set-profile-margin

POST /api/v1/portfolios/margin
Specify the margin override value for a portfolio to either increase notional requirements or opt-in to higher leverage.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    SetPortfolioMarginOverrideRequest request = new SetPortfolioMarginOverrideRequest.Builder().build();
    SetPortfolioMarginOverrideResponse response = portfoliosService.setPortfolioMarginOverride(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new SetPortfolioMarginOverrideRequest();
    var response = portfoliosService.SetPortfolioMarginOverride(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.SetMarginOverrideRequest{}
    response, err := portfoliosSvc.SetMarginOverride(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = SetMarginOverrideRequest()
    response = client.set_margin_override(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.updateMarginOverride({
        portfolioId: 'PORTFOLIO_ID_HERE',
        marginOverride: '0.1',
    }).then(async (response) => {
        console.log('Margin Override Updated: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl set-margin-override --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

