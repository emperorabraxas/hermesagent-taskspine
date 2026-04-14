# Create an end user
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/end-user-accounts/create-an-end-user

post /v2/end-users
Creates an end user. An end user is an entity that can own CDP EVM accounts, EVM smart accounts, and/or Solana accounts. 1 or more authentication methods must be associated with an end user. By default, no accounts are created unless the optional `evmAccount` and/or `solanaAccount` fields are provided.
This API is intended to be used by the developer's own backend, and is authenticated using the developer's CDP API key.


