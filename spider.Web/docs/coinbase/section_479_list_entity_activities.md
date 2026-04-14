# List Entity Activities
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/activities/list-entity-activities

GET /v1/entities/{entity_id}/activities
List all activities associated with a given entity.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    ActivitiesService activitiesService = PrimeServiceFactory.createActivitiesService(client);
    ListEntityActivitiesRequest request = new ListEntityActivitiesRequest("entity_id");
    ListEntityActivitiesResponse response = activitiesService.listEntityActivities(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var activitiesService = new ActivitiesService(client);

    var request = new GetActivityByActivityIdRequest("portfolio_id", "activity_id");

    var response = activitiesService.GetActivityByActivityId(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    activitiesService := activities.NewActivitiesService(client)

    request := &activities.GetActivityRequest{
        PortfolioId: "portfolio-id",
        Id:          "activity-id",
    }

    response, err := activitiesService.GetActivity(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetActivityRequest(
        portfolio_id="portfolio-id",
        activity_id="activity-id",
    )

    response = prime_client.get_activity(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-activity --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const activitiesService = new ActivitiesService(client);

    activitiesService.listEntityActivities({
        entityId: 'ENTITY_ID_HERE'
    }).then(async (response) => {
        console.log('Activities: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

