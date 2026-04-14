# Advanced Trade API Endpoints
Source: https://docs.cdp.coinbase.com/coinbase-business/advanced-trade-apis/rest-api



The Advanced Trade API lets you manage orders, portfolios, products, and fees with our new `v3` endpoints.

## Advanced Trade Endpoints

Advanced Trade endpoint URL: **`https://api.coinbase.com/api/v3/brokerage/{resource}`**

## Private Endpoints

Consult the [Authentication guide](/coinbase-app/authentication-authorization/api-key-authentication) for more information on CDP API keys.

| API                                                                                                                        | Method | Resource                               | API Key Permission                |
| :------------------------------------------------------------------------------------------------------------------------- | :----- | :------------------------------------- | :-------------------------------- |
| [List Accounts](/api-reference/advanced-trade-api/rest-api/accounts/list-accounts)                                         | GET    | `/accounts`                            | `view`                            |
| [Get Account](/api-reference/advanced-trade-api/rest-api/accounts/get-account)                                             | GET    | `/accounts/:account_id`                | `view`                            |
| [Create Order](/api-reference/advanced-trade-api/rest-api/orders/create-order)                                             | POST   | `/orders`                              | `trade`                           |
| [Cancel Orders](/api-reference/advanced-trade-api/rest-api/orders/cancel-order)                                            | POST   | `/orders/batch_cancel`                 | `trade`                           |
| [List Orders](/api-reference/advanced-trade-api/rest-api/orders/list-orders)                                               | GET    | `/orders/historical/batch`             | `view`                            |
| [List Fills](/api-reference/advanced-trade-api/rest-api/orders/list-fills)                                                 | GET    | `/orders/historical/fills`             | `view`                            |
| [Get Order](/api-reference/advanced-trade-api/rest-api/orders/get-order)                                                   | GET    | `/orders/historical/{order_id}`        | `view`                            |
| [Preview Orders](/api-reference/advanced-trade-api/rest-api/orders/preview-orders)                                         | POST   | `/orders/preview`                      | `view`                            |
| [Get Best Bid/Ask](/api-reference/advanced-trade-api/rest-api/products/get-best-bid-ask)                                   | GET    | `/best_bid_ask`                        | `view`                            |
| [Get Product Book](/api-reference/advanced-trade-api/rest-api/products/get-product-book)                                   | GET    | `/product_book`                        | `view`                            |
| [List Products](/api-reference/advanced-trade-api/rest-api/products/list-products)                                         | GET    | `/products`                            | `view`                            |
| [Get Product](/api-reference/advanced-trade-api/rest-api/products/get-product)                                             | GET    | `/products/{product_id}`               | `view`                            |
| [Get Product Candles](/api-reference/advanced-trade-api/rest-api/products/get-product-candles)                             | GET    | `/products/{product_id}/candles`       | `view`                            |
| [Get Market Trades](/api-reference/advanced-trade-api/rest-api/products/get-market-trades)                                 | GET    | `/products/{product_id}/ticker`        | `view`                            |
| [Get Transactions Summary](/api-reference/advanced-trade-api/rest-api/fees/get-transaction-summary)                        | GET    | `/transaction_summary`                 | `view`                            |
| [Create Convert Quote](/api-reference/advanced-trade-api/rest-api/convert/create-convert-quote)                            | POST   | `/convert/quote`                       | `trade`                           |
| [Commit Convert Trade](/api-reference/advanced-trade-api/rest-api/convert/commit-convert-trade)                            | POST   | `/convert/{trade_id}`                  | `trade`                           |
| [Get Convert Trade](/api-reference/advanced-trade-api/rest-api/convert/get-convert-trade)                                  | GET    | `/convert/{trade_id}`                  | `view`                            |
| [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                   | GET    | `/portfolios`                          | `view`                            |
| [Create Portfolio](/api-reference/advanced-trade-api/rest-api/portfolios/create-portfolio)                                 | POST   | `/portfolios`                          | `view` (any portfolio)            |
| [Move Portfolio Funds](/api-reference/advanced-trade-api/rest-api/portfolios/move-portfolios-funds)                        | POST   | `/portfolios`                          | `transfer` (for source portfolio) |
| [Get Portfolio Breakdown](/api-reference/advanced-trade-api/rest-api/portfolios/get-portfolio-breakdown)                   | GET    | `/portfolios`                          | `view` (for that portfolio)       |
| [Delete Portfolio](/api-reference/advanced-trade-api/rest-api/portfolios/delete-portfolio)                                 | DELETE | `/portfolios`                          | `trade` (for that portfolio)      |
| [Edit Portfolio](/api-reference/advanced-trade-api/rest-api/portfolios/edit-portfolio)                                     | PUT    | `/portfolios`                          | `trade` (for that portfolio)      |
| [Get Futures Balance Summary](/api-reference/advanced-trade-api/rest-api/futures/get-futures-balance-summary)              | GET    | `/cfm/balance_summary`                 | `view`                            |
| [List Futures Positions](/api-reference/advanced-trade-api/rest-api/futures/list-futures-positions)                        | GET    | `/cfm.positions`                       | `view`                            |
| [Get Futures Position](/api-reference/advanced-trade-api/rest-api/futures/get-futures-position)                            | GET    | `/cfm/positions/{product_id}`          | `view`                            |
| [Schedule Futures Sweep](/api-reference/advanced-trade-api/rest-api/futures/schedule-futures-sweep)                        | POST   | `/cfm/sweeps/schedule`                 | `transfer`                        |
| [List Futures Sweeps](/api-reference/advanced-trade-api/rest-api/futures/list-futures-sweeps)                              | GET    | `/cfm/sweeps`                          | `view`                            |
| [Cancel Futures Sweep](/api-reference/advanced-trade-api/rest-api/futures/cancel-pending-futures-sweep)                    | DELETE | `/cfm/sweeps`                          | `transfer`                        |
| [Get Intraday Margin Setting](/api-reference/advanced-trade-api/rest-api/futures/get-intraday-margin-setting)              | GET    | `/cfm/intraday/margin_setting`         | `view`                            |
| [Set Intraday Margin Setting](/api-reference/advanced-trade-api/rest-api/futures/set-intraday-margin-settings)             | POST   | `/cfm/intraday/margin_setting`         | `trade`                           |
| [Get Current Margin Window](/api-reference/advanced-trade-api/rest-api/futures/get-current-margin-window)                  | GET    | `/cfm/intraday/current_margin_window`  | `view`                            |
| [Get Perpetuals Portfolio Summary](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-portfolio-summary) | GET    | `/intx/portfolio`                      | `view` (for intx portfolio)       |
| [List Perpetuals Positions](/api-reference/advanced-trade-api/rest-api/perpetuals/list-perpetuals-positions)               | GET    | `/intx/positions`                      | `view` (for intx portfolio)       |
| [Get Perpetuals Position](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-position)                   | GET    | `/intx/positions`                      | `view` (for intx portfolio)       |
| [Get Perpetuals Portfolio Balances](/api-reference/advanced-trade-api/rest-api/perpetuals/get-portfolio-balances)          | GET    | `/intx/balances`                       | `view` (for intx portfolio)       |
| [Opt-In Multi Asset Collateral](/api-reference/advanced-trade-api/rest-api/perpetuals/opt-in-or-out)                       | POST   | `/intx/multi_asset_collateral`         | `trade` (for intx portfolio)      |
| [Allocate Portfolio](/api-reference/advanced-trade-api/rest-api/perpetuals/allocate-portfolio)                             | POST   | `/intx/allocate`                       | `transfer` (for intx portfolio)   |
| [List Payment Methods](/api-reference/advanced-trade-api/rest-api/payment-methods/list-payment-methods)                    | GET    | `/payment_methods`                     | `view`                            |
| [Get Payment Method](/api-reference/advanced-trade-api/rest-api/payment-methods/get-payment-method)                        | GET    | `/payment_methods/{payment_method_id}` | `view`                            |
| [Get Api Key Permissions](/api-reference/advanced-trade-api/rest-api/data-api/get-api-key-permissions)                     | GET    | `/key_permissions`                     | `view`                            |

## Public Endpoints

Public endpoints do not require authentication.

<Tip>
  1s cache is enabled for all public endpoints. If you need real-time data, please choose one of the following options:

  * Use the [WebSocket](/coinbase-app/advanced-trade-apis/websocket/websocket-overview) (recommended as this will provide the fastest product and market trades updates).
  * Set `cache-control: no-cache` header on the API requests to bypass caching.
  * Use the authenticated endpoints.
</Tip>

| API                                                                                                        | Method | Resource                                |
| :--------------------------------------------------------------------------------------------------------- | :----- | :-------------------------------------- |
| [Get Server Time](/api-reference/advanced-trade-api/rest-api/public/get-server-time)                       | GET    | `/time`                                 |
| [Get Public Product Book](/api-reference/advanced-trade-api/rest-api/public/get-public-product-book)       | GET    | `/market/product_book`                  |
| [List Public Products](/api-reference/advanced-trade-api/rest-api/public/list-public-products)             | GET    | `/market/products`                      |
| [Get Public Product](/api-reference/advanced-trade-api/rest-api/public/get-public-product)                 | GET    | `/market/products/{product_id}`         |
| [Get Public Product Candles](/api-reference/advanced-trade-api/rest-api/public/get-public-product-candles) | GET    | `/market/products/{product_id}/candles` |
| [Get Public Market Trades](/api-reference/advanced-trade-api/rest-api/public/get-public-market-trades)     | GET    | `/market/products/{product_id}/ticker`  |

