# Prime Conversions
Source: https://docs.cdp.coinbase.com/custom-stablecoins/prime-conversions



Convert between USDC and your custom stablecoin using the [Prime Conversion API](/api-reference/prime-api/rest-api/transactions/create-conversion). Conversions are instant, 1:1, and bidirectional — allowing movement between USDC and your custom stablecoin in either direction.

<Note>
  **Prime API vs. Stableswapper**: This page covers the **Prime API** path, which operates through Coinbase Prime's centralized infrastructure. If you need to swap tokens directly onchain (without Prime), see the [Stableswapper Quickstart](/custom-stablecoins/quickstart) instead.
</Note>

## Prerequisites

* A Coinbase Prime account with API credentials configured. See the [Prime Quickstart](/prime/introduction/quickstart) for setup instructions.
* Your portfolio ID and wallet ID. See [Wallets](/prime/concepts/wallets/wallets-overview) for how to retrieve these.

## Creating a conversion

Use the [Create Conversion](/api-reference/prime-api/rest-api/transactions/create-conversion) endpoint to convert between USDC and your custom stablecoin. Replace `CBTUSD` with your custom stablecoin symbol.

<Tabs>
  <Tab title="Python">
    ```python wrap theme={null}
    from prime_sdk.credentials import Credentials
    from prime_sdk.client import Client
    from prime_sdk.services.transactions import TransactionsService, CreateConversionRequest
    import uuid

    credentials = Credentials.from_env("PRIME_CREDENTIALS")
    client = Client(credentials)
    transactions_service = TransactionsService(client)

    request = CreateConversionRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
        amount='100',
        destination='DESTINATION_WALLET_UUID',
        idempotency_key=str(uuid.uuid4()),
        source_symbol='USDC',
        destination_symbol='CBTUSD',
    )

    response = transactions_service.create_conversion(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```ts wrap theme={null}
    const transactionsService = new TransactionsService(client);

    transactionsService.createConversion({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE',
        amount: "100",
        destination: "DESTINATION_WALLET_UUID",
        idempotencyKey: uuidv4(),
        sourceSymbol: "USDC",
        destinationSymbol: "CBTUSD",
    }).then(async (response) => {
        console.log('Conversion: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

For examples in Java, .NET, Go, and CLI, see the [Prime Conversions](/prime/concepts/stablecoins/conversions) guide.

## Tracking a conversion

Use the transaction ID returned by the Create Conversion endpoint to track its status via [Get Transaction by ID](/api-reference/prime-api/rest-api/transactions/get-transaction-by-transaction-id). Conversions typically reach a terminal state within a few seconds.

For code examples on tracking transactions, see the [Prime Conversions](/prime/concepts/stablecoins/conversions#tracking-a-stablecoin-conversion) guide.

## What to read next

<CardGroup>
  <Card title="Prime Withdrawals" icon="arrow-right-from-bracket" href="/custom-stablecoins/prime-withdrawals">
    Withdraw converted custom stablecoins to an onchain wallet
  </Card>

  <Card title="Stableswapper Quickstart" icon="rocket" href="/custom-stablecoins/quickstart">
    Swap tokens directly onchain via the Stableswapper program
  </Card>
</CardGroup>

