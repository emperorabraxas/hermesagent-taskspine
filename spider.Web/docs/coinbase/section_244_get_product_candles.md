# Get product candles
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles

GET /products/{product_id}/candles
Historic rates for a product. Rates are returned in grouped buckets. Candle schema is of the form `[timestamp, price_low, price_high, price_open, price_close]`

<Warning>
  * Historical rate data may be incomplete. No data is published for intervals where there are no ticks.
  * Historical rates should *not* be polled frequently. For real-time info, use the trade and book endpoints in conjunction with the WebSocket feed.
</Warning>

## Time Range

If the `start` or `end` fields are not provided, both fields are ignored. If a custom time range is not declared, then one ending now is selected.

The `granularity` field must be one of the following "second" values: `{60, 300, 900, 3600, 21600, 86400}`, or your request is rejected. These values correspond to timeslices representing one minute, five minutes, fifteen minutes, one hour, six hours, and one day, respectively.

If data points are readily available, your response may contain as many as `300` candles and some of those candles may precede your declared `start` value.

## Max Candles

<Info>
  The maximum number of data points for a single request is `300` candles.
</Info>

If your selection of start/end time and granularity results in more than `300` data points, your request is rejected. To retrieve fine granularity data over a larger time range, you must make multiple requests with new start/end ranges.

## Response Items

Each bucket is an array of the following information:

* `time` bucket start time
* `low` lowest price during the bucket interval
* `high` highest price during the bucket interval
* `open` opening price (first trade) in the bucket interval
* `close` closing price (last trade) in the bucket interval
* `volume` volume of trading activity during the bucket interval

