# Sign a message
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/solana-accounts/sign-a-message

post /v2/solana/accounts/{address}/sign/message
Signs an arbitrary message with the given Solana account.

**WARNING:** Never sign a message that you didn't generate, as it can be an arbitrary transaction. For example, it might send all of your funds to an attacker.


