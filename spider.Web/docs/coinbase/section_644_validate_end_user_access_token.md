# Validate end user access token
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/end-user-accounts/validate-end-user-access-token

post /v2/end-users/auth/validate-token
Validates the end user's access token and returns the end user's information. Returns an error if the access token is invalid or expired.

This API is intended to be used by the developer's own backend, and is authenticated using the developer's CDP API key.


