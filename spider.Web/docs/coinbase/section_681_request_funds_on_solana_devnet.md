# Request funds on Solana devnet
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/faucets/request-funds-on-solana-devnet

post /v2/solana/faucet
Request funds from the CDP Faucet on Solana devnet.

Faucets are available for SOL, USDC, and CBTUSD.

To prevent abuse, we enforce rate limits within a rolling 24-hour window to control the amount of funds that can be requested.
These limits are applied at both the CDP Project level and the blockchain address level.
A single blockchain address cannot exceed the specified limits, even if multiple users submit requests to the same address.

| Token  | Amount per Faucet Request |Rolling 24-hour window Rate Limits|
|:-----: |:-------------------------:|:--------------------------------:|
| SOL    | 0.00125 SOL               | 0.0125 SOL                       |
| USDC   | 1 USDC                    | 10 USDC                          |
| CBTUSD | 1 CBTUSD                  | 10 CBTUSD                        |



