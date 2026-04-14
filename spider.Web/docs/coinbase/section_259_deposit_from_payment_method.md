# Deposit from payment method
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/transfers/deposit-from-payment-method

POST  /deposits/payment-method
Deposits funds from a linked external payment method to the specified `profile_id`.

<Info>
  **Deposit funds from a payment method**

  See [Get all payment methods](/api-reference/exchange-api/rest-api/transfers/get-all-payment-methods). The SEPA payment method is not allowed for depositing funds because it is a push payment method.
</Info>

## API Key Permissions

This endpoint requires the "transfer" permission. API key must belong to default profile.

