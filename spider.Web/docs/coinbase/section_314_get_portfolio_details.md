# Get portfolio details
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-portfolio-details

GET  /api/v1/portfolios/{portfolio}/detail
Retrieves the summary, positions, and balances of a portfolio.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    GetPortfolioDetailRequest request = new GetPortfolioDetailRequest.Builder()
        .portfolio("portfolio_id")
        .build();
    GetPortfolioDetailResponse response = portfoliosService.getPortfolioDetail(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new GetPortfolioDetailsRequest(
        Portfolio: "portfolio_id",
    );
    var response = portfoliosService.GetPortfolioDetails(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.GetPortfolioDetailsRequest{
        Portfolio: "portfolio_id",
    }
    response, err := portfoliosSvc.GetPortfolioDetails(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetPortfolioDetailsRequest(
        portfolio="portfolio_id",
    )
    response = client.get_portfolio_details(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getPortfolioDetails({
        portfolio: 'PORTFOLIO_ID_HERE',
    }).then(async (response) => {
        console.log('Portfolio Details: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-portfolio-details --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

