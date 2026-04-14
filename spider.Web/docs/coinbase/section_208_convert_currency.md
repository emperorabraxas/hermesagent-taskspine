# Convert currency
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/conversions/convert-currency

POST /conversions
Converts funds from `from` currency to `to` currency. Funds are converted on the `from` account in the `profile_id` profile.

<Warning>
  **Caution**

  Users whose USD and USDC accounts are unified do not have access to the conversion endpoint, and conversions from USDC to USD are automatic upon deposit.
</Warning>

## API Key Permissions

This endpoint requires the "trade" permission.

## Response

A successful conversion is assigned a conversion ID. The corresponding ledger entries for a conversion reference this conversion ID.

