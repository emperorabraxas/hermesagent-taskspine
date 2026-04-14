# Get all accounts for a profile
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/accounts/get-all-account-profile

GET /accounts
Get a list of trading accounts from the profile of the API key.

<Info>
  **Info**

  Your trading accounts are separate from your Coinbase accounts. See [Deposit from Coinbase account](/api-reference/exchange-api/rest-api/transfers/deposit-from-coinbase-account) for documentation on how to deposit funds to begin trading.
</Info>

## API Key Permissions

This endpoint requires either the "view" or "trade" permission.

## Rate Limits

This endpoint has a custom rate limit by profile ID: 25 requests per second, up to 50 requests per second in bursts

