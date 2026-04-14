# Cancel an order
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/orders/cancel-an-order

DELETE /orders/{order_id}
Cancel a single open order by `{id}`.

<Info>
  Cancel a previously placed order

  The order must belong to the profile that the API key belongs to. If the order had no matches during its lifetime, its record may be purged. This means the order details is not available with `GET /orders/<id>`.
</Info>

<Warning>
  To prevent a race condition when canceling an order, it is highly recommended that you specify the product id as a query string.
</Warning>

## API Key Permissions

This endpoint requires the "trade" permission.

Orders can be canceled using either the exchange assigned `id` or the client assigned `client_oid`. When using `client_oid` it must be preceded by the `client:` namespace.

## Response

A successfully cancelled order response includes:

* the order ID if the order is cancelled with the exchange assigned `id`,
* the client assigned `client_oid` if the order is cancelled with client order ID.

## Cancel Reject

If the order could not be canceled (already filled or previously canceled, etc.), then an error response indicates the reason in the `message` field.

