# Get repayment preview XM
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/loan/get-repayment-preview-xm

GET /loans/repayment-preview-xm
Preview the results of a loan principal repayment for a cross margin user.

Preview the results of a loan principal repayment for a cross margin user. This endpoint shows the before and after state of your lending overview when repaying a loan.

<Info>
  **Repayment Preview for Cross Margin (XM) Users**

  Use this endpoint to preview how repaying a loan would affect your cross margin account's margin requirements, account equity, and other lending metrics before actually making the repayment.
</Info>

<Warning>
  **Caution**

  The lending rate limit is [10 RPS per profile](/exchange/rest-api/rate-limits).
</Warning>

