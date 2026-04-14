# Get all known trading pairs
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-all-known-trading-pairs

GET /products
Gets a list of available currency pairs for trading.

<Warning>
  **Order Size Limits Removed**

  The properties `base_max_size`, `base_min_size`, `max_market_funds` were [removed on June 30](/exchange/changes/changelog#2022-jun-30).

  The property, `min_market_funds`, has been repurposed as the notional minimum size for limit orders.
</Warning>

The `base_min_size` and `base_max_size` fields define the min and max order size.

The `min_market_funds` and `max_market_funds` fields define the min and max funds allowed in a market order.

`status_message` provides any extra information regarding the status if available.

The `quote_increment` field specifies the min order price as well as the price increment.

The order price must be a multiple of this increment (i.e. if the increment is 0.01, order prices of 0.001 or 0.021 would be rejected).

The `base_increment` field specifies the minimum increment for the `base_currency`.

`trading_disabled` indicates whether trading is currently restricted on this product, this includes whether both new orders and order cancellations are restricted.

`cancel_only` indicates whether this product only accepts cancel requests for orders.

`post_only` indicates whether only maker orders can be placed. No orders will be matched when post\_only mode is active.

`limit_only` indicates whether this product only accepts limit orders.

Only a maximum of one of `trading_disabled`, `cancel_only`, `post_only`, `limit_only` can be true at once. If none are true, the product is trading normally.

`fx_stablecoin` indicates whether the currency pair is a Stable Pair.

`auction_mode` boolean which indicates whether or not the book is in auction mode. For more details on the auction mode see [Get product book](/api-reference/exchange-api/rest-api/products/get-product-book) describing the level 1 book which contains information pertaining to products in auction mode.

<Info>
  When limit\_only is true, matching can occur if a limit order crosses the book. Product ID will not change once assigned to a product but all other fields ares subject to change.
</Info>

