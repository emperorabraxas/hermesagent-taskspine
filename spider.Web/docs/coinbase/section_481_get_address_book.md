# Get Address Book
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/address-book/get-address-book

GET /v1/portfolios/{portfolio_id}/address_book
Gets a list of address book addresses.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    AddressBookService addressBookService = PrimeServiceFactory.createAddressBookService(client);

    GetPortfolioAddressBookRequest request = new GetPortfolioAddressBookRequest.Builder("portfolio_id").build();

    GetPortfolioAddressBookResponse response = addressBookService.getAddressBook(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var addressBookService = new AddressBookService(client);

    var request = new GetPortfolioAddressBookRequest("portfolio_id");

    var response = addressBookService.GetPortfolioAddressBook(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    addressBookService := addressbook.NewAddressBookService(client)

    request := &addressbook.GetAddressBookRequest{
        PortfolioId: "portfolio-id",
    }

    response, err := addressBookService.GetAddressBook(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = GetAddressBookRequest(
            portfolio_id="portfolio_id",
    )

    response = prime_client.get_address_book(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl get-address-book --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const addressBooksService = new AddressBooksService(client);

    addressBooksService.listAddressBooks({
        portfolioId: 'PORTFOLIO_ID_HERE'
    }).then(async (response) => {
        console.log('Address Book: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

