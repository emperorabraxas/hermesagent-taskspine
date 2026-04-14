# List Invoices
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/invoice/list-invoices

GET /v1/entities/{entity_id}/invoices
Retrieve a list of invoices belonging to an entity.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    InvoiceService invoiceService = PrimeServiceFactory.createInvoiceService(client);

    ListInvoicesRequest request = new ListInvoicesRequest.Builder("ENTITY_ID_HERE").build();

    ListInvoicesResponse response = invoiceService.listInvoices(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var invoiceService = new InvoiceService(client);

    var request = new ListInvoicesRequest("ENTITY_ID_HERE");

    var response = invoiceService.ListInvoices(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    invoiceService := invoice.NewInvoiceService(client)

    request := &invoice.ListInvoicesRequest{
        EntityId: "ENTITY_ID_HERE",
    }

    response, err := invoiceService.ListInvoices(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = ListInvoicesRequest(
        entity_id="ENTITY_ID_HERE",
    )

    response = prime_client.list_invoices(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl list-invoices --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const invoicesService = new InvoicesService(client);

    invoicesService.listInvoices({
        entityId: 'ENTITY_ID_HERE'
    }).then(async (response) => {
        console.log('Invoices: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

