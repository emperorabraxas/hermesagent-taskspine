# Get lending overview
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/loan/get-lending-overview

GET /loans/lending-overview
This API summarizes lending for a given client. It calculates the overall loan balance, collateral level, and amounts available to borrow. It also returns any withdrawal restrictions in force on the client.

Get lending overview returns all amounts in USD notional values, except available\_per\_asset mappings which are returned in both notional and native values.

<Info>
  **Coinbase Exchange Loans Program**

  See [Coinbase Exchange Loans Program](https://coinbase.bynder.com/m/47c334b9a63ed3e4/original/exchange-Loans-Program.pdf) for program details including qualification criteria and sample terms.
</Info>

<Warning>
  **Caution**

  The lending rate limit is [10 RPS per profile](/exchange/rest-api/rate-limits).
</Warning>

