# Request funds on EVM test networks
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/faucets/request-funds-on-evm-test-networks

post /v2/evm/faucet
Request funds from the CDP Faucet on supported EVM test networks.

Faucets are available for ETH, USDC, EURC, and cbBTC on Base Sepolia and Ethereum Sepolia, and for ETH only on Ethereum Hoodi.

To prevent abuse, we enforce rate limits within a rolling 24-hour window to control the amount of funds that can be requested.
These limits are applied at both the CDP User level and the blockchain address level.
A single blockchain address cannot exceed the specified limits, even if multiple users submit requests to the same address.

| Token | Amount per Faucet Request |Rolling 24-hour window Rate Limits|
|:-----:|:-------------------------:|:--------------------------------:|
| ETH   | 0.0001 ETH                | 0.1 ETH                          |
| USDC  | 1 USDC                    | 10 USDC                          |
| EURC  | 1 EURC                    | 10 EURC                          |
| cbBTC | 0.0001 cbBTC              | 0.001 cbBTC                      |



