# Withdraw to crypto address
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/transfers/withdraw-to-crypto-address

POST /withdrawals/crypto
Withdraws funds from the specified `profile_id` to an external crypto address

## API Key Permissions

This endpoint requires the "transfer" permission. API key must belong to default profile.

## Travel Rule

The Travel Rule requires financial institutions, including custodial cryptocurrency exchanges, to share basic information about their customers when sending funds over a certain amount. VASPs that are part of the TRUST consortium use the [TRUST solution](https://www.coinbase.com/travelrule) when sharing PII to satisfy the Travel Rule data requirements.

For more details and examples, see [Travel Rule for Withdrawals](/exchange/travel-rule/withdrawals).

