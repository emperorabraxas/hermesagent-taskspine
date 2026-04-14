# Create session token
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/onramp-offramp/create-session-token

POST /v1/token
Creates a single use token that can be used to initialize an Onramp or Offramp session.
 This API should be called once for every new user session. The returned token will expire after 5 minutes.


