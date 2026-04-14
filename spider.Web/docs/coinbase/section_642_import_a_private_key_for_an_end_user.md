# Import a private key for an end user
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/end-user-accounts/import-a-private-key-for-an-end-user

post /v2/end-users/import
Imports an existing private key for an end user into the developer's CDP Project. The private key must be encrypted using the CDP SDK's encryption scheme before being sent to this endpoint. This API should be called from the [CDP SDK](https://github.com/coinbase/cdp-sdk) to ensure that the associated private key is properly encrypted.

This endpoint allows developers to import existing keys for their end users, supporting both EVM and Solana key types. The end user must have at least one authentication method configured.


