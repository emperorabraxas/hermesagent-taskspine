# Get loan preview XM
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/loan/get-loan-preview-xm

GET /loans/loan-preview-xm
Preview the results of a loan for a cross margin user.

Preview the results of a loan for a cross margin user. This endpoint shows the before and after state of your lending overview when taking out a new loan.

<Info>
  **Loan Preview for Cross Margin (XM) Users**

  Use this endpoint to preview how a new loan would affect your cross margin account's margin requirements, account equity, and other lending metrics before actually opening the loan.
</Info>

<Warning>
  **Caution**

  The lending rate limit is [10 RPS per profile](/exchange/rest-api/rate-limits).
</Warning>

