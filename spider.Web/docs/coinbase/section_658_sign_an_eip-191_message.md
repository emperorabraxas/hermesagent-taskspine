# Sign an EIP-191 message
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/evm-accounts/sign-an-eip-191-message

post /v2/evm/accounts/{address}/sign/message
Signs an [EIP-191](https://eips.ethereum.org/EIPS/eip-191) message with the given EVM account.

Per the specification, the message in the request body is prepended with `0x19 <0x45 (E)> <thereum Signed Message:\n" + len(message)>` before being signed.


