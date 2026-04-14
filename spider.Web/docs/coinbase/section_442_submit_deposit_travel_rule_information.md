# Submit deposit travel rule information
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/transfers-under-development/submit-deposit-travel-rule-information

post /v2/transfers/{transferId}/travel-rule
Submit travel rule information for a deposit transfer held pending compliance review.

Required fields vary by jurisdiction and may include originator name, address, date of birth, personal ID, and VASP information.

If the submitted information satisfies all jurisdictional requirements, `status` will be `completed` and the transfer will proceed. Otherwise, `status` will be `incomplete` and `missingFields` will indicate which fields still need to be provided.


