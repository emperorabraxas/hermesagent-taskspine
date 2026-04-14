# Get address transaction history
Source: https://docs.cdp.coinbase.com/api-reference/rest-api/addresses/get-address-transaction-history

GET /v1/networks/{network_id}/addresses/{address_id}/transactions
List of all transactions that have interacted with a given external address. Interaction types: native, ERC20 and ERC721 transfer activities. The transactions are returned in reverse chronological order based on their block height.


