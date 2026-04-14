# Get wrapped asset conversion rate
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/wrapped-assets/get-wrapped-asset-conversion-rate

GET /wrapped-assets/{wrapped_asset_id}/conversion-rate
Returns the conversion rate of a wrapped asset

### Testing

You can test the `cbETH` conversion rate by sending an HTTP GET request to the following URL:

[https://api.exchange.coinbase.com/wrapped-assets/CBETH/conversion-rate](https://api.exchange.coinbase.com/wrapped-assets/CBETH/conversion-rate)

### Response

#### 200 Success

A successful request responds with HTTP status code 200 (OK) and the JSON response body has the following form:

```json lines wrap theme={null}
{
  "amount": "1.001374669367288075"
}
```

The `amount` field in the response body is the number of `ETH2` units that can be exchanged for 1 `cbETH`.

#### 429 Failure

This endpoint can be queried at most once a second.

If queried more than once a second, the failed request responds with HTTP status code 429 ([Too Many Requests](https://docs.w3cub.com/http/status/429)) and the JSON response body has the following form:

```json lines wrap theme={null}
{
  "message": "Public rate limit exceeded"
}
```

<Tip>
  Coinbase recommends that you repeatedly query the API, sleeping 1 second in between queries, to get conversion rate updates (currently updated 1x a day) as soon as possible without exceeding the rate limit.
</Tip>

