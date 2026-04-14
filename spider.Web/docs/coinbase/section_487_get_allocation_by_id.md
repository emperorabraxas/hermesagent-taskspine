# Get Allocation by ID
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/allocations/get-allocation-by-id

GET /v1/portfolios/{portfolio_id}/allocations/{allocation_id}
Retrieve an allocation by allocation ID.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    AllocationsService allocationsService = PrimeServiceFactory.createAllocationsService(client);

    GetAllocationRequest request = new GetAllocationRequest.Builder("PORTFOLIO_ID_HERE", "ALLOCATION_ID_HERE").build();

    GetAllocationResponse response = allocationsService.getAllocation(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var allocationsService = new AllocationsService(client);

    var request = new GetAllocationRequest("PORTFOLIO_ID_HERE", "ALLOCATION_ID_HERE");
    var response = allocationsService.GetAllocation(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    allocationsService := allocations.NewAllocationsService(client)

    request := &allocations.GetPortfolioAllocationRequest{
        PortfolioId:  "PORTFOLIO_ID_HERE",
        AllocationId: "ALLOCATION_ID_HERE",
    }

    response, err := allocationsService.GetPortfolioAllocation(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetAllocationByIdRequest(
            portfolio_id="PORTFOLIO_ID_HERE",
            allocation_id="ALLOCATION_ID_HERE",
    )

    response = prime_client.get_allocation_by_id(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-allocation --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const allocationService = new AllocationService(client);

    allocationService.getAllocation({
        allocationId: "ALLOCATION_ID_HERE",
        portfolioId: "PORTFOLIO_ID_HERE"
    }).then(async (response) => {
        console.log('Allocation: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

