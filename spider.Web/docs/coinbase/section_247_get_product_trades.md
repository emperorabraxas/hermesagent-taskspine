# Get product trades
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-trades

GET /products/{product_id}/trades
Gets a list the latest trades for a product.

## Side

The `side` of a trade indicates the maker order side. The maker order is the order that was open on the order book.

A `buy` side indicates a down-tick because the maker was a buy order and their order was removed. A `sell` side indicates an up-tick.

## Pagination

This request is paginated. See [Pagination](/exchange/rest-api/pagination) for more information.

