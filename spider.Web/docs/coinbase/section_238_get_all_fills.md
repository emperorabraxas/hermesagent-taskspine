# Get all fills
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/orders/get-all-fills

GET /fills
Get a list of fills. A fill is a partial or complete match on a specific order.

Get a list of recent fills of the API key's profile.

## API Key Permissions

This endpoint requires either the "view" or "trade" permission.

## Settlement and Fees

Fees are recorded in two stages. Immediately after the matching engine completes a match, the fill is inserted into our datastore. Once the fill is recorded, a settlement process settles the fill and credit both trading counterparties.

The `fee` field indicates the fees charged for this individual fill.

### Liquidity

The `liquidity` field indicates if the fill was the result of a liquidity provider or liquidity taker. `M` indicates Maker and `T` indicates Taker.

### Pagination

Fills are returned sorted by descending `trade_id` from the largest `trade_id` to the smallest `trade_id`. The `CB-BEFORE` header has this first trade ID so that future requests using the `cb-before` parameter fetch fills with a greater trade ID (newer fills).

See [Pagination](/exchange/rest-api/pagination) for more information.

