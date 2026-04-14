# Advanced Trade API Sandbox
Source: https://docs.cdp.coinbase.com/coinbase-business/advanced-trade-apis/sandbox



Advanced Trade API offers a static sandbox environment and its use cases are:

* Users can make API requests to Advanced sandbox API without authentication.
* Users can make API requests to the sandbox and get the same formatted responses as production.
* All responses are static and pre-defined.
* Set custom request header "X-Sandbox:" to trigger pre-defined variance in some endpoints.

## Advanced Trade Sandbox Endpoints

Advanced Trade sandbox endpoint URL: **`https://api-sandbox.coinbase.com/api/v3/brokerage/{resource}`**

<Info>
  Only Accounts and Orders related endpoints are currently available in the sandbox. All responses are mocked but have the same format as production.
</Info>

## Endpoints

The following table shows available Endpoints.

| API                                                                                                                        | Method | Resource                                    |
| :------------------------------------------------------------------------------------------------------------------------- | :----- | :------------------------------------------ |
| [List Accounts](/api-reference/advanced-trade-api/rest-api/accounts/list-accounts)                                         | GET    | `/accounts`                                 |
| [Get Account](/api-reference/advanced-trade-api/rest-api/accounts/get-account)                                             | GET    | `/accounts/{account_id}`                    |
| [Create Order](/api-reference/advanced-trade-api/rest-api/orders/create-order)                                             | POST   | `/orders`                                   |
| [Cancel Orders](/api-reference/advanced-trade-api/rest-api/orders/cancel-order)                                            | POST   | `/orders/batch_cancel`                      |
| [Edit Order](/api-reference/advanced-trade-api/rest-api/orders/edit-order)                                                 | POST   | `/orders/edit`                              |
| [Edit Order Preview](/api-reference/advanced-trade-api/rest-api/orders/edit-order-preview)                                 | POST   | `/orders/edit_preview`                      |
| [List Orders](/api-reference/advanced-trade-api/rest-api/orders/list-orders)                                               | GET    | `/orders/historical/batch`                  |
| [List Fills](/api-reference/advanced-trade-api/rest-api/orders/list-fills)                                                 | GET    | `/orders/historical/fills`                  |
| [Get Order](/api-reference/advanced-trade-api/rest-api/orders/get-order)                                                   | GET    | `/orders/historical/{order_id}`             |
| [Preview Order](/api-reference/advanced-trade-api/rest-api/orders/preview-orders)                                          | POST   | `/orders/preview`                           |
| [Close Position](/api-reference/advanced-trade-api/rest-api/orders/close-position)                                         | POST   | `/orders/close_position`                    |
| [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                   | GET    | `/portfolios`                               |
| [Allocate Portfolio](/api-reference/advanced-trade-api/rest-api/perpetuals/allocate-portfolio)                             | POST   | `intx/allocate`                             |
| [Get Perpetuals Portfolio Summary](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-portfolio-summary) | GET    | `/intx/portfolio/{portfolio_uuid}`          |
| [List Perpetuals Positions](/api-reference/advanced-trade-api/rest-api/perpetuals/list-perpetuals-positions)               | GET    | `/intx/positions/{portfolio_uuid}`          |
| [Get Perpetuals Position](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-position)                   | GET    | `/intx/positions/{portfolio_uuid}/{symbol}` |
| [Get Portfolios Balances](/api-reference/advanced-trade-api/rest-api/perpetuals/get-portfolio-balances)                    | GET    | `/intx/balances/{portfolio_uuid}`           |
| [Opt In or Out of Multi Asset Collateral](/api-reference/advanced-trade-api/rest-api/perpetuals/opt-in-or-out)             | POST   | `/intx/multi_asset_collateral`              |

<br />

The following table shows Endpoints with available request parameters.

| API                                                                                                                        | Method | Resource                                    | Request Parameters                                                                                                                                               |
| :------------------------------------------------------------------------------------------------------------------------- | :----- | :------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Get Account](/api-reference/advanced-trade-api/rest-api/accounts/get-account)                                             | GET    | `/accounts/{account_id}`                    | **account\_id** retrieved from [List Accounts](/api-reference/advanced-trade-api/rest-api/accounts/list-accounts)                                                |
| [Get Order](/api-reference/advanced-trade-api/rest-api/orders/get-order)                                                   | GET    | `/orders/historical/{order_id}`             | **order\_id**: retrieved from [List Orders](/api-reference/advanced-trade-api/rest-api/orders/list-orders)                                                       |
| [List Orders](/api-reference/advanced-trade-api/rest-api/orders/list-orders)                                               | GET    | `/orders/historical/batch`                  | **order\_status**: CANCELLED/OPEN                                                                                                                                |
| [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                   | GET    | `/portfolios`                               | **portfolio\_type**: DEFAULT/CONSUMER/INTX                                                                                                                       |
| [Allocate Portfolio](/api-reference/advanced-trade-api/rest-api/perpetuals/allocate-portfolio)                             | POST   | `intx/allocate`                             | **portfolio\_uuid**: retrieved from [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                     |
| [Get Perpetuals Portfolio Summary](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-portfolio-summary) | GET    | `/intx/portfolio/{portfolio_uuid}`          | **portfolio\_uuid**: retrieved from [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                     |
| [List Perpetuals Positions](/api-reference/advanced-trade-api/rest-api/perpetuals/list-perpetuals-positions)               | GET    | `/intx/positions/{portfolio_uuid}`          | **portfolio\_uuid**: retrieved from [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                     |
| [Get Perpetuals Position](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-position)                   | GET    | `/intx/positions/{portfolio_uuid}/{symbol}` | **portfolio\_uuid**: retrieved from [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)<br />**symbol**: e.g. ETH-PERP-INTX |
| [Get Portfolios Balances](/api-reference/advanced-trade-api/rest-api/perpetuals/get-portfolio-balances)                    | GET    | `/intx/balances/{portfolio_uuid}`           | **portfolio\_uuid**: retrieved from [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                     |
| [Opt In or Out of Multi Asset Collateral](/api-reference/advanced-trade-api/rest-api/perpetuals/opt-in-or-out)             | POST   | `/intx/multi_asset_collateral`              | **portfolio\_uuid**: retrieved from [List Portfolios](/api-reference/advanced-trade-api/rest-api/portfolios/list-portfolios)                                     |

<br />

The following table shows available Endpoints returning error responses with required headers.

| API                                                                                        | Method | Resource               | Error                       | Header                                        |
| :----------------------------------------------------------------------------------------- | :----- | :--------------------- | :-------------------------- | :-------------------------------------------- |
| [Create Order](/api-reference/advanced-trade-api/rest-api/orders/create-order)             | POST   | `/orders`              | INSUFFICIENT\_FUND          | "X-Sandbox: PostOrder\_insufficient\_fund"    |
| [Cancel Orders](/api-reference/advanced-trade-api/rest-api/orders/cancel-order)            | POST   | `/orders/batch_cancel` | UNKNOWN\_CANCEL\_ORDER      | "X-Sandbox: CancelOrders\_failure"            |
| [Edit Order](/api-reference/advanced-trade-api/rest-api/orders/edit-order)                 | POST   | `/orders/edit`         | ORDER\_NOT\_FOUND           | "X-Sandbox: EditOrder\_failure"               |
| [Edit Order Preview](/api-reference/advanced-trade-api/rest-api/orders/edit-order-preview) | POST   | `/orders/edit_preview` | ORDER\_NOT\_FOUND           | "X-Sandbox: PreviewEditOrder\_failure"        |
| [Preview Order](/api-reference/advanced-trade-api/rest-api/orders/preview-orders)          | POST   | `/orders/preview`      | PREVIEW\_INSUFFICIENT\_FUND | "X-Sandbox: PreviewOrder\_insufficient\_fund" |

<br />

**See Also:**

* [REST API Overview](/coinbase-app/advanced-trade-apis/rest-api)

