# Get a single account's holds
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/accounts/get-single-account-hold

GET /accounts/{account_id}/holds
List the holds of an account that belong to the same profile as the API key. Holds are placed on an account for any active orders or pending withdraw requests. As an order is filled, the hold amount is updated. If an order is canceled, any remaining hold is removed. For withdrawals, the hold is removed after it is completed.

## Pagination

This request is paginated. See [Pagination](/exchange/rest-api/pagination) for more information.

