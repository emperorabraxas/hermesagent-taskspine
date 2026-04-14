# Get new loan preview
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/loan/get-new-loan-preview

GET /loans/loan-preview
This API is similar to lending-overview but is used to preview the results of opening a new loan. The values returned in the preview response take the existing loans, collateral and the potential change being previewed into account. Note the preview request accepts native currency amounts as input.

<Info>
  **Coinbase Exchange Loans Program**

  See [Coinbase Exchange Loans Program](https://coinbase.bynder.com/m/47c334b9a63ed3e4/original/exchange-Loans-Program.pdf) for program details including qualification criteria and sample terms.
</Info>

<Warning>
  **Caution**

  The lending rate limit is [10 RPS per profile](/exchange/rest-api/rate-limits).
</Warning>

