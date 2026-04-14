# Cancel all orders
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/orders/cancel-all-orders

DELETE /orders
With best effort, cancel all open orders. This may require you to make the request multiple times until all of the open orders are deleted.

## API Key Permissions

This endpoint requires the "trade" permission.

## Examples

| Example                      | Response                                 |
| :--------------------------- | :--------------------------------------- |
| `/orders?product_id=FOO-BAR` | (404) ProductNotFound                    |
| `/orders?product_id=BtC-uSd` | (200) Cancel all orders for BTC-USD      |
| `/orders?Product_id=BTC-USD` | (400) Return BadRequest Error            |
| `/orders`                    | (200) Cancel all orders for all products |

