# Get a single account's ledger
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/accounts/get-single-account-ledger

GET /accounts/{account_id}/ledger
Lists ledger activity for an account. This includes anything that would affect the accounts balance - transfers, trades, fees, etc.

<Warning>
  **Caution**

  If neither `start_date` nor `end_date` is set, the endpoint will return ledger activity for the past 1 day only.
</Warning>

List account activity of the API key's profile. Account activity either increases or decreases your account balance.

## API Key Permissions

This endpoint requires either the "view" or "trade" permission.

## Entry Types

Entry type indicates the reason for the account change.

| Type       | Description                                                              |
| ---------- | ------------------------------------------------------------------------ |
| transfer   | Funds moved to/from Coinbase to Coinbase Exchange                        |
| match      | Funds moved as a result of a trade                                       |
| fee        | Fee as a result of a trade                                               |
| rebate     | Fee rebate as per our [fee schedule](https://exchange.coinbase.com/fees) |
| conversion | Funds converted between fiat currency and a stablecoin                   |

## Details

If an entry is the result of a trade (match, fee), the details field contains additional information about the trade.

## Pagination

Items are paginated and sorted latest first. See [Pagination](/exchange/rest-api/pagination) for retrieving additional entries after the first page.

## Searching By Date

Searching by start and end dates are inclusive of the time provided and can be combined with before or after fields to narrow down the search to entries from a specific time range. Dates must be after Unix Epoch time and are restricted to the following formats:

* [RFC3339](https://www.rfc-editor.org/rfc/rfc3339) (i.e., `2006-01-02T15:04:05.000000Z` or `2006-01-02T15:04:05+05:30`)
* `2006-01-02`
* `2006-01-02T15:04:05`

A `400 Bad Request` error is returned for any formats that are not accepted.

