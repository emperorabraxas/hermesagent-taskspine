# Open new loan
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/loan/open-new-loan

POST /loans/open
This API triggers a loan open request. Funding is not necessarily instantaneous and there is no SLA. You are notified when funds have settled in your Exchange account. Loan open requests, once initiated, cannot be canceled.

<Info>
  **Coinbase Exchange Loans Program**

  See [Coinbase Exchange Loans Program](https://coinbase.bynder.com/m/47c334b9a63ed3e4/original/exchange-Loans-Program.pdf) for program details including qualification criteria and sample terms.
</Info>

<Warning>
  **Caution**

  The lending rate limit is [10 RPS per profile](/exchange/rest-api/rate-limits).
</Warning>

