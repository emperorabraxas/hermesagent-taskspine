# Get all orders
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/orders/get-all-orders

GET /orders
List your current open orders. Only open or un-settled orders are returned by default. As soon as an order is no longer open and settled, it will no longer appear in the default request. Open orders may change state between the request and the response depending on market conditions.

## Pending Orders

Orders with a "pending" status have fewer fields in the response.

* Pending limit orders do not have `stp`, `time_in_force`, `expire_time`, and `post_only`.
* Pending market orders have the same fields as a pending limit order minus `price` and `size`, and no market specific fields (`funds`, `specified_funds`).
* Pending stop orders have the same fields as a pending limit order and no stop specific fields (`stop`, `stop_price`).

| Order Type           | Does Not Have These Fields                                                                      |
| :------------------- | :---------------------------------------------------------------------------------------------- |
| Pending Limit Order  | `stp`, `time_in_force`, `expire_time`, `post_only`                                              |
| Pending Market Order | `stp`, `time_in_force`, `expire_time`, `post_only`, `price`, `size`, `funds`, `specified_funds` |
| Pending Stop Order   | `stp`, `time_in_force`, `expire_time`, `post_only`, `stop`, `stop_price`                        |

## API Key Permissions

This endpoint requires either the "view" or "trade" permission.

<Tip>
  To specify multiple statuses, use the status query argument multiple times: `/orders?status=done&status=pending`.
</Tip>

## Order Status and Settlement

Orders which are no longer resting on the order book, are marked with the `done` status. There is a small window between an order being `done` and `settled`. An order is settled when all of the fills have settled and the remaining holds (if any) have been removed.

## Polling

For high-volume trading it is strongly recommended that you maintain your own list of open orders and use one of the streaming market data feeds to keep it updated. You should poll the open orders endpoint once when you start trading to obtain the current state of any open orders.

`executed_value` is the cumulative match `size` \* `price` and is only present for orders placed after 2016-05-20.

<Info>
  Open orders can change state between the request and the response depending on market conditions.
</Info>

## Pagination

This request is paginated. See [Pagination](/exchange/rest-api/pagination) for more information.

