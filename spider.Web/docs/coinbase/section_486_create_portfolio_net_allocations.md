# Create Portfolio Net Allocations
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/allocations/create-portfolio-net-allocations

POST /v1/allocations/net
Create net allocation for a given portfolio.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    AllocationsService allocationsService = PrimeServiceFactory.createAllocationsService(client);

    String allocationId = UUID.randomUUID().toString();
    String allocationLegId = UUID.randomUUID().toString();

    AllocationLeg allocationLeg = new AllocationLeg.Builder()
            .allocationLegId(allocationLegId)
            .amount("100")
            .destinationPortfolioId("DESTINATION_PORTFOLIO_ID_HERE")
            .build();

    CreateNetAllocationRequest request = new CreateNetAllocationRequest.Builder()
            .sourcePortfolioId("SOURCE_PORTFOLIO_ID_HERE")
            .allocationId(allocationId)
            .allocationLegs(new AllocationLeg[]{allocationLeg})
            .productId("ETH-USD")
            .nettingId("NETTING_ID_HERE")
            .build();

    CreateNetAllocationResponse response = allocationsService.createNetAllocation(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var allocationsService = new AllocationsService(client);

    var allocationId = Guid.NewGuid();
    var allocationLegId = Guid.NewGuid();

    var allocationLeg = new AllocationLeg()
    {
        AllocationLegId = allocationLegId.ToString(),
        Amount = "100",
        DestinationPortfolioId = "ADD_DESTINATION_PORTFOLIO_ID_HERE",
    };

    var request = new CreateNetAllocationRequest()
    {
        AllocationId = allocationId.ToString(),
        ProductId = "ETH-USD",
        SourcePortfolioId = "ADD_SOURCE_PORTFOLIO_ID_HERE",
        AllocationLegs = [ allocationLeg ],
        SizeType = Prime.Model.SizeType.PERCENT,
        NettingId = "NETTING_ID_HERE",
    };

    var response = allocationsService.CreateNetAllocation(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    allocationsService := allocations.NewAllocationsService(client)

    allocationId := uuid.New().String()
    allocationLegId := uuid.New().String()

    allocationLeg := &model.AllocationLeg{
        LegId:                  allocationLegId,
        DestinationPortfolioId: "DESTINATION_PORTFOLIO_ID_GOES_HERE",
        Amount:                 "100.0",
    }

    request := &allocations.CreatePortfolioNetAllocationsRequest{
        AllocationId:      allocationId,
        SourcePortfolioId: "SOURCE_PORTFOLIO_ID_GOES_HERE",
        ProductId:         "ETH-USD",
        AllocationLegs:    []*model.AllocationLeg{allocationLeg},
        OrderIds:          []string{"ORDER_IDS_TO_BE_ALLOCATED_HERE"},
        SizeType:          "PERCENT",
        NettingId:         "NETTING_ID_HERE",
    }

    response, err := allocationsService.CreatePortfolioNetAllocations(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    allocation_id = uuid.uuid4()
    allocation_leg_id = uuid.uuid4()

    product_id = 'ETH-USD'
    size_type = 'PERCENT'

    allocation_leg = AllocationLeg(
        leg_id=allocation_leg_id,
        destination_portfolio_id='DESTINATION_PORTFOLIO_ID_GOES_HERE',
        amount='100.0',
    )

    request = CreatePortfolioNetAllocationsRequest(
        allocation_id=allocation_id,
        source_portfolio_id='SOURCE_PORTFOLIO_ID_GOES_HERE',
        product_id=product_id,
        order_ids=['ORDER_ID_GOES_HERE'],
        allocation_legs=[allocation_leg],
        size_type=size_type,
        netting_id='NETTING_ID_HERE',
    )

    response = prime_client.create_portfolio_net_allocations(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl create-net-allocation --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const allocationService = new AllocationService(client);

    allocationService.createNetAllocation({
        allocationId: uuidv4(),
        sourcePortfolioId: "SOURCE_PORTFOLIO_ID_GOES_HERE"
        productId: "ETH-USD",
        orderIds: ["ORDER_ID_GOES_HERE"],
        allocationLegs: [{
            legId:                  uuidv4(),
            destinationPortfolioId: "DESTINATION_PORTFOLIO_ID_GOES_HERE",
            amount:                 "100.0",
        }]
        sizeType: AllocationSizeType.Percent,
        nettidId: uuidv4()
    }).then(async (response) => {
        console.log('Order allocated: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

