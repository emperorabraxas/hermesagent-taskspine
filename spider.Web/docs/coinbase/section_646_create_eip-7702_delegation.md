# Create EIP-7702 delegation
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/evm-accounts/create-eip-7702-delegation

post /v2/evm/accounts/{address}/eip7702/delegation
Creates an EIP-7702 delegation for an EVM EOA account, upgrading it with smart account capabilities.

This endpoint:
- Retrieves delegation artifacts from onchain
- Signs the EIP-7702 authorization for delegation
- Assembles and submits a Type 4 transaction
- Creates an associated smart account object

The delegation allows the EVM EOA to be used as a smart account, which enables batched transactions and gas sponsorship via paymaster.


