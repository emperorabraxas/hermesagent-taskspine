# Create Address Book Entry
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/address-book/create-address-book-entry

POST /v1/portfolios/{portfolio_id}/address_book
Creates an entry for a portfolio's trusted addresses.

Use the Prime SDK or CLI to test this endpoint by following the [quickstart](/prime/introduction/quickstart) guide and running with the following examples

<Tabs>
  <Tab title="Java">
    ```java theme={null}
    AddressBookService addressBookService = PrimeServiceFactory.createAddressBookService(client);

    CreateAddressBookEntryRequest request = new CreateAddressBookEntryRequest.Builder("portfolio_id")
            .accountIdentifier("account_identifier")
            .address("address")
            .currencySymbol("currency_symbol")
            .name("name")
            .build();

    CreateAddressBookEntryResponse response = addressBookService.createAddressBookEntry(request);
    ```

    For more information, please visit the [Prime Java SDK](https://github.com/coinbase-samples/prime-sdk-java).
  </Tab>

  <Tab title=".NET">
    ```csharp wrap theme={null}
    var addressBookService = new AddressBookService(client);

    var request = new CreateAddressBookEntryRequest("portfolio_id")
    {
        Address = "address",
        CurrencySymbol = "currency_symbol",
        Name = "name",
        AccountIdentifier = "account_identifier",
    };

    var response = addressBookService.CreateAddressBookEntry(request);
    ```

    For more information, please visit the [Prime .NET SDK](https://github.com/coinbase-samples/prime-sdk-dotnet).
  </Tab>

  <Tab title="Go">
    ```go wrap theme={null}
    addressBookService := addressbook.NewAddressBookService(client)

    request := &addressbook.CreateAddressBookEntryRequest{
        PortfolioId: "portfolio-id",
        Address: "address",
        Symbol: "currency_symbol",
        Name: "name",
        AccountIdentifier: "account_identifier",
    }

    response, err := addressBookService.CreateAddressBookEntry(context.Background(), request)
    ```

    For more information, please visit the [Prime Go SDK](https://github.com/coinbase-samples/prime-sdk-go).
  </Tab>

  <Tab title="Python">
    ```python wrap theme={null}
    prime_client = PrimeClient(credentials)

    request = CreateAddressBookEntryRequest(
        portfolio_id="portfolio_id",
        address="address",
        currency_symbol="currency_symbol",
        name="name",
        account_identifier="account_identifier",
    )

    response = prime_client.get_address_book(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="CLI">
    ```bash wrap theme={null}
    primectl create-address-book-entry --help
    ```

    For more information, please visit the [Prime CLI](https://github.com/coinbase-samples/prime-cli).
  </Tab>

  <Tab title="TS/JS">
    ```typescript wrap theme={null}
    const addressBooksService = new AddressBooksService(client);

    addressBooksService.createAddressBook({
        portfolioId: 'PORTFOLIO_ID_HERE',
        address: 'ADDRESS_HERE',
        currencySymbol: 'ETH',
        name: 'XYZ Address',
    }).then(async (response) => {
        console.log('Address Book: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

