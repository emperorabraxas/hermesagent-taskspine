# Get onramp user limits
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/onramp/get-onramp-user-limits

post /v2/onramp/limits
Returns the transaction limits for an onramp user based on their payment method and user identifier. Use this API to show users their remaining purchase capacity before initiating an onramp transaction.
Currently supports `GUEST_CHECKOUT_APPLE_PAY` payment method with phone number identification. The phone number must have been previously verified via OTP.


