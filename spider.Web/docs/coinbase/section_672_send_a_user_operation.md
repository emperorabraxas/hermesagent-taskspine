# Send a user operation
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/evm-smart-accounts/send-a-user-operation

post /v2/evm/smart-accounts/{address}/user-operations/{userOpHash}/send
Sends a user operation with a signature.
The payload to sign must be the `userOpHash` field of the user operation. This hash should be signed directly (not using `personal_sign` or EIP-191 message hashing).
The signature must be 65 bytes in length, consisting of: - 32 bytes for the `r` value - 32 bytes for the `s` value - 1 byte for the `v` value (must be 27 or 28)
If using the CDP Paymaster, the user operation must be signed and sent within 2 minutes of being prepared.


