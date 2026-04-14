# Get single order
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/orders/get-single-order

GET /orders/{order_id}
Get a single order by `id`.

## API Key Permissions

This endpoint requires either the "view" or "trade" permission.

Orders can be queried using either the exchange assigned `id` or the client assigned `client_oid`. When using `client_oid` it must be preceded by the `client:` namespace.

If the order is canceled, and if the order had no matches, the response might return the status code `404`.

<Info>
  Open orders can change state between the request and the response depending on market conditions.
</Info>

