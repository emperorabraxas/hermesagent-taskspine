# Get principal repayment preview
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/loan/get-principal-repayment-preview

GET /loans/repayment-preview
Preview the results of a loan principal repayment.

Like the Get lending overview API, all values are notional except `available_per_asset` which returns both notional and native values per currency.

<Info>
  **Coinbase Exchange Loans Program**

  See [Coinbase Exchange Loans Program](https://coinbase.bynder.com/m/47c334b9a63ed3e4/original/exchange-Loans-Program.pdf) for program details including qualification criteria and sample terms.
</Info>

<Warning>
  **Caution**

  The lending rate limit is [10 RPS per profile](/exchange/rest-api/rate-limits).
</Warning>

