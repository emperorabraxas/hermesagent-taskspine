# Metadata
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/transfers/metadata



Store custom key-value pairs on transfers to track your own references like invoice IDs, customer IDs, or order numbers. Use metadata to connect transfers with your internal systems for reconciliation, reporting, and business intelligence.

<Note>
  **Status:** Not yet implemented

  The metadata field is defined in the API spec but is not currently functional. This documentation describes the intended behavior once implementation is complete.
</Note>

## Constraints and limitations

| Property                   | Constraint                         |
| -------------------------- | ---------------------------------- |
| Maximum key-value pairs    | 50 per transfer                    |
| Maximum key length         | 40 characters                      |
| Maximum value length       | 500 characters                     |
| Immutable                  | Yes (cannot be updated or deleted) |
| Searchable/filterable      | No                                 |
| Included in webhook events | No                                 |

<Warning>
  Never store sensitive data like passwords, account numbers, or PII in metadata.
</Warning>

## Usage

To add metadata, send your key-value pairs when using [Create a Transfer](/api-reference/payment-apis/rest-api/transfers-under-development/create-a-transfer). Include the optional `metadata` field in your request body.

**Request:**

```json highlight={13-16} theme={null}
{
  "source": {
    "accountId": "account_123",
    "asset": "usd"
  },
  "target": {
    "email": "user@example.com",
    "asset": "usd"
  },
  "amount": "100.00",
  "asset": "usd",
  "execute": true,
  "metadata": {
    "invoiceId": "INV-001",
    "customerId": "cust_123"
  }
}
```

**Response:**

```json highlight={4-7} theme={null}
{
  "transferId": "transfer_123",
  "status": "processing",
  "metadata": {
    "invoiceId": "INV-001",
    "customerId": "cust_123"
  },
  ...
}
```

## Retrieving metadata

Metadata is included automatically when you retrieve transfers. No additional API calls are needed.

**Get a single transfer:**

```bash theme={null}
GET /v2/transfers/{transferId}
```

**List all transfers:**

```bash theme={null}
GET /v2/transfers
```

**Example response:**

```json highlight={4-7} theme={null}
{
  "transferId": "transfer_123",
  "status": "completed",
  "metadata": {
    "invoiceId": "INV-001",
    "customerId": "cust_123"
  },
  ...
}
```

The metadata persists throughout the transfer lifecycle and is returned in all subsequent API calls.

## Best practices

* **Use consistent key names** across transfers (`invoiceId` not `invoice_id`) for easier querying in your own systems
* **Store IDs, not full data** to reference your system's records instead of duplicating information
* **Keep keys concise** since keys are limited to 40 characters

## Related endpoints

* [Create a Transfer](/api-reference/payment-apis/rest-api/transfers-under-development/create-a-transfer)
* [Get a Transfer](/api-reference/payment-apis/rest-api/transfers-under-development/get-a-transfer)
* [List Transfers](/api-reference/payment-apis/rest-api/transfers-under-development/list-transfers)

