# Add an EVM smart account to an end user
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/end-user-accounts/add-an-evm-smart-account-to-an-end-user

post /v2/end-users/{userId}/evm-smart-account
Creates an EVM smart account for an existing end user. The backend will create a new EVM EOA account to serve as the owner of the smart account.
This API is intended to be used by the developer's own backend, and is authenticated using the developer's CDP API key.


