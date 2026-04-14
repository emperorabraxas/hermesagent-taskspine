# Create a new stake-wrap
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/wrapped-assets/create-new-stake-wrap

POST /wrapped-assets/stake-wrap
Stakes and wraps `from_currency` to `to_currency`. Funds are stake-wrapped in the profile associated with the API key.

## API Key Permissions​

This endpoint requires the "trade" permission.

## Response​

A successful stake-wrap is assigned a stake-wrap ID. The corresponding ledger entries for a stake-wrap reference this stake-wrap ID.

<Tip>
  **More Details**

  For more information on stake-wrapping ETH (`from_currency`) to CBETH (`to_currency`), see [How to stake/wrap ETH to CBETH](https://coinbase.bynder.com/m/5d3cff1b03f8aeb0/original/exchange-CBETH-Stake-Wrap-Instructions.pdf).
</Tip>

