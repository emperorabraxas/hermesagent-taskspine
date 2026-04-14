# List loans
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/loan/list-loans

GET /loans
Accepts zero or more loan IDs as input. If no loan IDs are specified, it returns all loans for the user. Otherwise it returns only the loan IDs specified.

<Info>
  **Coinbase Exchange Loans Program**

  See [Coinbase Exchange Loans Program](https://coinbase.bynder.com/m/47c334b9a63ed3e4/original/exchange-Loans-Program.pdf) for program details including qualification criteria and sample terms.
</Info>

<Warning>
  **Caution**

  The lending rate limit is [10 RPS per profile](/exchange/rest-api/rate-limits).
</Warning>

