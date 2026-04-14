# Prime Withdrawals
Source: https://docs.cdp.coinbase.com/custom-stablecoins/prime-withdrawals



After converting USDC to your custom stablecoin via the [Prime Conversion API](/custom-stablecoins/prime-conversions), you can withdraw the tokens to an onchain wallet using the [Create Withdrawal](/api-reference/prime-api/rest-api/transactions/create-withdrawal) endpoint. This sends the custom stablecoin from your Prime custody to a blockchain address you control.

<Note>
  **Prime API vs. Stableswapper**: This page covers the **Prime API** withdrawal path, which moves tokens from Coinbase Prime custody to an onchain wallet. If your tokens are already onchain, use the [Stableswapper](/custom-stablecoins/quickstart) to swap directly between USDC and your custom stablecoin.
</Note>

## Prerequisites

* A Coinbase Prime account with API credentials configured. See the [Prime Quickstart](/prime/introduction/quickstart) for setup instructions.
* Your portfolio ID and wallet ID. See [Wallets](/prime/concepts/wallets/wallets-overview) for how to retrieve these.
* The destination address must be added to your Prime address book. See [Adding to the address book](/prime/concepts/transactions/withdrawals#adding-to-the-address-book) for setup instructions.

## Creating a withdrawal

Use the [Create Withdrawal](/api-reference/prime-api/rest-api/transactions/create-withdrawal) endpoint to withdraw your custom stablecoin to an onchain wallet. Replace `CBTUSD` with your custom stablecoin symbol.

<Tabs>
  <Tab title="Python">
    ```python wrap theme={null}
    from prime_sdk.credentials import Credentials
    from prime_sdk.client import Client
    from prime_sdk.services.transactions import TransactionsService, CreateWithdrawalRequest, BlockchainAddress
    import uuid

    credentials = Credentials.from_env("PRIME_CREDENTIALS")
    client = Client(credentials)
    transactions_service = TransactionsService(client)

    request = CreateWithdrawalRequest(
        portfolio_id="PORTFOLIO_ID_HERE",
        wallet_id="WALLET_ID_HERE",
        amount='100',
        destination_type='DESTINATION_BLOCKCHAIN',
        idempotency_key=str(uuid.uuid4()),
        currency_symbol='CBTUSD',
        blockchain_address=BlockchainAddress(
            address='DESTINATION_WALLET_ADDRESS',
        ),
    )

    response = transactions_service.create_withdrawal(request)
    ```

    For more information, please visit the [Prime Python SDK](https://github.com/coinbase-samples/prime-sdk-py).
  </Tab>

  <Tab title="TS/JS">
    ```ts wrap theme={null}
    const transactionsService = new TransactionsService(client);

    transactionsService.createWithdrawal({
        portfolioId: 'PORTFOLIO_ID_HERE',
        walletId: 'WALLET_ID_HERE',
        amount: "100",
        idempotencyKey: uuidv4(),
        currencySymbol: "CBTUSD",
        destinationType: DestinationType.DestinationBlockchain,
        blockchainAddress: {
            address: 'DESTINATION_WALLET_ADDRESS',
        }
    }).then(async (response) => {
        console.log('Withdrawal: ', response);
    })
    ```

    For more information, please visit the [Prime TS SDK](https://github.com/coinbase-samples/prime-sdk-ts).
  </Tab>
</Tabs>

For examples in Java, .NET, Go, and CLI, see the [Prime Withdrawals](/prime/concepts/transactions/withdrawals) guide.

## Approval workflow

By default, all Prime withdrawals require consensus approval in the Prime UI before completion. The API response includes:

* A **Transaction ID** for tracking the withdrawal
* An **Activity ID** specific to the consensus process in Prime

Approval requirements can be adjusted in the Prime UI — these settings apply to **all operations** (both API and UI). For more granular control, the Custom Stablecoins team can help configure per-API-key approval requirements. Self-service configuration for per-API-key approvals is coming soon.

## Tracking a withdrawal

Use the transaction ID returned by the Create Withdrawal endpoint to track its status via [Get Transaction by ID](/api-reference/prime-api/rest-api/transactions/get-transaction-by-transaction-id). You can also use [List Transactions](/api-reference/prime-api/rest-api/transactions/list-portfolio-transactions) with a `WITHDRAWAL` filter to list all withdrawal transactions.

For code examples on tracking transactions, see the [Prime Withdrawals](/prime/concepts/transactions/withdrawals#tracking-withdrawals) guide.

## What to read next

<CardGroup>
  <Card title="Prime Conversions" icon="arrows-rotate" href="/custom-stablecoins/prime-conversions">
    Convert between USDC and your custom stablecoin via Prime API
  </Card>

  <Card title="Stableswapper Quickstart" icon="rocket" href="/custom-stablecoins/quickstart">
    Swap tokens directly onchain via the Stableswapper program
  </Card>
</CardGroup>

