# Deposit Destinations
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/deposit-destinations-under-development/deposit-destinations-under-development



Deposit Destinations allow you to manage where funds can be deposited into your accounts. There are two types of deposit destinations: crypto and fiat.

## Crypto Deposit Destinations

Crypto deposit destinations are cryptocurrency addresses that you can generate and fetch via the API. Once created, these addresses can receive cryptocurrency payments on their specified network and will settle in your account balance.

**Metadata:**
You can attach metadata to any deposit destination you create to track the purpose or source of deposits.

**Example:**

```json theme={null}
{
  "depositDestinationId": "depositDestination_123",
  "accountId": "account_456",
  "type": "crypto",
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "network": "base",
  "metadata": {
    "customer_id": "cust_789",
    "reference": "order-12345"
  }
}
```

Use the list endpoint to retrieve all deposit destinations.

