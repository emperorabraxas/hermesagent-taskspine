# List Activities
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/activities/list-activities

GET /v1/portfolios/{portfolio_id}/activities
List all activities associated with a given portfolio.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    ActivitiesService activitiesService = PrimeServiceFactory.createActivitiesService(client);
    ListActivitiesRequest request = new ListActivitiesRequest.Builder("portfolio_id").build();
    ListActivitiesResponse listActivitiesResponse = activitiesService.listActivities(request);ctivityByActivityIdResponse response = activitiesService.getActivityByActivityId(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var activitiesService = new ActivitiesService(client);
    var list = new ListActivitiesRequest("portfolio_id");
    var response = activitiesService.ListActivities(list);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    activitiesService := activities.NewActivitiesService(client)

    request := &activities.ListActivitiesRequest{
        PortfolioId: credentials.PortfolioId,
    }

    response, err := activitiesService.ListActivities(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListActivitiesRequest(
        portfolio_id="portfolio_id"
    )
    response = prime_client.list_activities(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-activities --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const activitiesService = new ActivitiesService(client);

    activitiesService.listPortfolioActivities({
        portfolioId: 'PORTFOLIO_ID_HERE'
    }).then(async (response) => {
        console.log('Activities: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

