# Get position for portfolio/instrument
Source: https://docs.cdp.coinbase.com/api-reference/international-exchange-api/rest-api/portfolios/get-position-portfolio

GET /api/v1/portfolios/{portfolio}/positions/{instrument}
Retrieves the position for a given portfolio and symbol.

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    PortfoliosService portfoliosService = IntxServiceFactory.createPortfoliosService(client);
    GetPositionForPortfolioInstrumentRequest request = new GetPositionForPortfolioInstrumentRequest.Builder()
        .portfolio("portfolio_id")
        .instrument("BTC-USDC")
        .build();
    GetPositionForPortfolioInstrumentResponse response = portfoliosService.getPositionForPortfolioInstrument(request);
    ```

    For more information, please visit the [INTX Java SDK](https://github.com/coinbase-samples/intx-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```cs theme={null}
    var portfoliosService = new PortfoliosService(client);
    var request = new GetPositionForPortfolioInstrumentRequest(
        Portfolio: "portfolio_id",
        Instrument: "BTC-USDC",
    );
    var response = portfoliosService.GetPositionForPortfolioInstrument(request);
    ```

    For more information, please visit the [INTX .NET SDK](https://github.com/coinbase-samples/intx-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    portfoliosSvc := portfolios.NewPortfoliosService(client)
    request := &portfolios.GetInstrumentPositionRequest{
        Portfolio: "portfolio_id",
        Instrument: "BTC-USDC",
    }
    response, err := portfoliosSvc.GetInstrumentPositionRequest(context.Background(), request)
    ```

    For more information, please visit the [INTX Go SDK](https://github.com/coinbase-samples/intx-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    client = IntxClient()
    request = GetPositionForPortfolioInstrumentRequest(
        portfolio="portfolio_id",
        instrument="BTC-USDC",
    )
    response = client.get_position_for_portfolio_instrument(request)
    ```

    For more information, please visit the [INTX Python SDK](https://github.com/coinbase-samples/intx-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```js theme={null}
    const portfoliosService = new PortfoliosService(client);

    portfoliosService.getInstrumentPosition({
        portfolio: 'PORTFOLIO_ID_HERE',
        instrument: 'ETH-USDC',
    }).then(async (response) => {
        console.log('Portfolio Instrument: ', response);
    })
    ```

    For more information, please visit the [INTX TS SDK](https://github.com/coinbase-samples/intx-sdk-ts).
  </Tab>

  <Tab title="CLI">
    ```
    intxctl get-position-for-instrument --help
    ```

    For more information, please visit the [INTX CLI](https://github.com/coinbase-samples/intx-cli).
  </Tab>
</Tabs>

