# Get wrapped asset details
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/wrapped-assets/get-wrapped-asset-details

GET /wrapped-assets/{wrapped_asset_id}
Returns the circulating and total supply of a wrapped asset, and its conversion rate

### Properties

#### Circulating Supply

The number of wrapped asset units in possession of customers. It *excludes* units pre-minted and held in abeyance to quickly serve wrapping customers.

Circulating supply is the most appropriate input to determine the market capitalization of a wrapped asset.

#### Total Supply

The total number of wrapped asset units that have been minted and exist on-chain.

#### Conversion Rate

The number of underlying staked units that can be exchanged for 1 wrapped asset (e.g., the number of ETH2 units per 1 cbETH unit).

#### Implied APY

Current annualized percentage yield earned as the net rewards by the staked ETH underlying cbETH. This estimate is based on the past 7 days of staking performance and is updated daily. For more details, refer to the "rate calculation" section of the [cbETH whitepaper](https://www.coinbase.com/cbeth/whitepaper).

### Response

#### 200 Success

A successful request responds with HTTP status code 200 (OK) and the JSON response body has the following form:

```json lines wrap theme={null}
{
  "circulating_supply": "288918.5085968099228762",
  "total_supply": "1021881.5038440099228762",
  "conversion_rate": "1.0213397911189787"
}
```

#### 429 Failure

This endpoint can be queried at most once a second.

If queried more than once a second, the failed request responds with HTTP status code 429 (Too Many Requests) and the JSON response body has the following form:

```json lines wrap theme={null}
{
  "message": "Public rate limit exceeded"
}
```

<Tip>
  Coinbase recommends that you repeatedly query the API, sleeping 1 second in between queries, to get conversion rate updates (currently updated 1x a day) as soon as possible without exceeding the rate limit.
</Tip>

