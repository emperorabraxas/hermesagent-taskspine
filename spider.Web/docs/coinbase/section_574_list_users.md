# List Users
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/users/list-users

GET /v1/entities/{entity_id}/users
List all users associated with a given entity.

<Info>
  **Entity ID**

  To retrieve your entity\_id, use [List Portfolios](/api-reference/prime-api/rest-api/portfolios/list-portfolios).
</Info>

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    UsersService usersService = PrimeServiceFactory.createUsersService(client);

    ListUsersRequest request = new ListUsersRequest.Builder()
        .entityId("ENTITY_ID_HERE")
        .build();

    ListUsersResponse response = usersService.listUsers(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var usersService = new UsersService(client);

    var request = new ListUsersRequest("ENTITY_ID_HERE");

    var response = usersService.ListUsers(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    usersService := users.NewUsersService(client)

    request := &users.ListEntityUsersRequest{
        EntityId: "ENTITY_ID_HERE",
    }

    response, err := usersService.ListEntityUsers(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListUsersRequest(
        entity_id="ENTITY_ID_HERE",
    )

    response = prime_client.list_users(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-entity-users --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const usersService = new UsersService(client);

    usersService.listUsers({
        entityId: 'ENTITY_ID_HERE'
    }).then(async (response) => {
        console.log('Users: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

