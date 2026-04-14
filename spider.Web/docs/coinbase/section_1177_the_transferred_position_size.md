# The transferred position size
 'position_size': '0.0001',
 'status': 'PROCESSED',
 'transfer_type': 'POSITION_TRANSFER',
 'transfer_uuid': '0a6d7eb3-d544-35bd-9c2b-9af98fa50d77',
 'updated_at': '2025-11-13T19:07:50Z'}
```

### 2025-NOV-18

#### Spot Order Routing to Coinbase Exchange: Addendum for REST API's `List instruments`, `Get instrument details`, `Get quote per instrument` endpoints

The following only applies for spot instruments configured to route spot orders to Coinbase Exchange.

###### List instruments, Get instrument details

`notional_24hr`, `avg_daily_notional`, `avg_30day_notional`, `quote → limit_up`, and `quote → limit_down` will be temporarily set to 0. This value is a placeholder and does not represent actual data. These fields will be deprecated and no longer populated in a future release.

The following field will be added for all instruments:

| Property            | Type   | Description                                                                                                                                                                           |
| :------------------ | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| execution\_exchange | string | For spot instruments configured to route orders to Coinbase Exchange, this is set to `COINBASE_EXCHANGE`. For all other instruments, this is set to `COINBASE_INTERNATIONAL_EXCHANGE` |

###### Get quote per instrument

`limit_up`, and `limit_down` will be temporarily set to 0. This value is a placeholder and does not represent actual data. These fields will be deprecated and no longer populated in a future release.

### 2025-NOV-13

#### Spot Order Routing to Coinbase Exchange

Introducing support to route spot orders to rest and match on equivalent Coinbase Exchange books.

Unless otherwise noted, the following only applies for spot instruments configured to route orders to Coinbase Exchange, orders routed to Coinbase Exchange, or fills on orders routed to Coinbase Exchange.

Where noted, "forwarded" properties indicate that Coinbase International Exchange will publish data from Coinbase Exchange. For example, in the REST API's List Instruments endpoint, for spot instruments configured to route orders to Coinbase Exchange, the `qty_24hr` property is forwarded, meaning it will represent the 24 hour trading volume for the instrument on Coinbase Exchange rather than on Coinbase International Exchange. For data returned by Coinbase Exchange, please refer to the [Coinbase Exchange API documentation](https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/introduction).

##### REST API

###### List instruments, Get instrument details

The following only applies for spot instruments configured to route spot orders to Coinbase Exchange.

| Property                 | Type   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :----------------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| qty\_24hr                | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| avg\_daily\_qty          | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| previous\_day\_qty       | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| trading\_state           | string | New available options include: `AUCTION_MODE`, `CANCEL_ONLY`, `POST_ONLY`, `LIMIT_ONLY`, `TRADING_DISABLED`, `CANCEL_ONLY_ENFORCED_BY_COINBASE_INTERNATIONAL_EXCHANGE`, `COINBASE_EXCHANGE_UNREACHABLE`<br /><br />All new options, except for the following, are forwarded from Coinbase Exchange. `CANCEL_ONLY_ENFORCED_BY_COINBASE_INTERNATIONAL_EXCHANGE` means Coinbase International Exchange only permits order cancellation separately from Coinbase Exchange. `COINBASE_EXCHANGE_UNREACHABLE` means the Coinbase International Exchange component is unable to establish connectivity with Coinbase Exchange |
| notional\_24hr           | string | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| avg\_daily\_notional     | string | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| quote → best\_bid\_price | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| quote → best\_ask\_price | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| quote → best\_bid\_size  | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| quote → best\_ask\_size  | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| quote → trade\_price     | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| quote → trade\_size      | string | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| quote → limit\_up        | string | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| quote → limit\_down      | string | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

###### Get quote per instrument

The following only applies for spot instruments configured to route spot orders to Coinbase Exchange.

| Property         | Type   | Description                      |
| :--------------- | :----- | :------------------------------- |
| best\_bid\_price | string | Forwarded from Coinbase Exchange |
| best\_ask\_price | string | Forwarded from Coinbase Exchange |
| best\_bid\_size  | string | Forwarded from Coinbase Exchange |
| best\_bid\_size  | string | Forwarded from Coinbase Exchange |
| trade\_price     | string | Forwarded from Coinbase Exchange |
| trade\_size      | string | Forwarded from Coinbase Exchange |
| limit\_up        | string | Will not be populated            |
| limit\_down      | string | Will not be populated            |

###### Get daily trading volumes

The following only applies for spot instruments configured to route spot orders to Coinbase Exchange.

| Property                              | Type   | Description                                                       |
| :------------------------------------ | :----- | :---------------------------------------------------------------- |
| instruments → notional                | string | Will not be populated                                             |
| totals → total\_instruments\_volume   | string | Excludes spot instruments which route orders to Coinbase Exchange |
| totals → total\_instruments\_notional | string | Excludes spot instruments which route orders to Coinbase Exchange |
| totals → total\_exchange\_volume      | string | Excludes spot instruments which route orders to Coinbase Exchange |
| totals → total\_exchange\_notional    | string | Excludes spot instruments which route orders to Coinbase Exchange |

###### Get aggregated candles data per instrument

Not supported for spot instruments configured to route orders to Coinbase Exchange.

###### Create order, Get order details, Cancel order, Cancel orders

The following only applies for orders routed to Coinbase Exchange.

| Property | Type   | Description                                   |
| :------- | :----- | :-------------------------------------------- |
| text     | string | Value may be forwarded from Coinbase Exchange |

###### List fills by portfolios

The following only applies for fills executed on Coinbase Exchange.

| Property         | Type   | Description                                                                                                                                                                                                                                                                                                                         |
| :--------------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| execution\_venue | string | The following values for fills executed on Coinbase Exchange will be added:<br /><br />`COINBASE_EXCHANGE_CLOB` for fills executed by Coinbase Exchange's central limit order book<br />`COINBASE_EXCHANGE_RFQ` for fills executed by Coinbase Exchange's request for quote engine<br /><br />Existing values will remain unchanged |

##### FIX API, Order Entry & Drop Copy

###### ExecutionReport (35=8)

The following only applies for orders routed to Coinbase Exchange. A few `OrdRejReason` values previously included in the `Upcoming Changes` page will not be added because they already exist in the XML spec.

| Tag  | Name         | Type   | Required | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| :--- | :----------- | :----- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 103  | OrdRejReason | int    | C        | For spot orders routed to Coinbase Exchange, new potential values include:<br /><br />49 = BROKER<br />51 = EXCHANGE\_CLOSED<br />52 = ORDER\_EXCEEDS\_LIMIT<br />53 = TOO\_LATE\_TO\_ENTER<br />55 = DUPLICATE\_OF\_A\_VERBALLY\_COMMUNICATED\_ORDER<br />56 = STALE\_ORDER<br />57 = TRADE\_ALONG\_REQUIRED<br />58 = INVALID\_INVESTOR\_ID<br />59 = UNSUPPORTED\_ORDER\_CHARACTERISTIC<br />60 = SURVEILLENCE\_OPTION<br />61 = INCORRECT\_ALLOCATED\_QUANTITY<br />62 = UNKNOWN\_ACCOUNT<br />64 = COINBASE\_EXCHANGE\_DEPOSIT\_FAILED                                                                                                               |
| 1430 | VenueType    | char   | N        | The following existing values for orders executed on Coinbase International Exchange will be renamed to:<br /><br />E = COINBASE\_INTERNATIONAL\_EXCHANGE\_ELECTRONIC\_EXCHANGE<br />N = COINBASE\_INTERNATIONAL\_EXCHANGE\_QUOTE\_NEGOTIATION<br /><br />The following values for spot orders routed to Coinbase Exchange will be added:<br /><br />X = COINBASE\_EXCHANGE\_ELECTRONIC\_EXCHANGE<br />Q = COINBASE\_EXCHANGE\_QUOTE\_NEGOTIATION<br /><br />Values suffixed with ELECTRONIC\_EXCHANGE indicate trades which occur on the central limit order book (CLOB). Values suffixed with QUOTE\_NEGOTIATION indicate trades through an RFQ process |
| 58   | Text         | string | N        | Value may be forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

###### OrderCancelReject (35=9)

The following only applies for spot orders routed to Coinbase Exchange. A few `OrdRejReason` values previously included in the `Upcoming Changes` page will not be added because they already exist in the XML spec.

| Tag | Name         | Type   | Required | Notes                                                                                                                                                                                                                                                        |
| :-- | :----------- | :----- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 102 | CxlRejReason | int    | N        | For spot orders routed to Coinbase Exchange, new potential values include:<br /><br />27 = BROKER<br />28 = UNABLE\_TO\_PROCESS\_ORDER\_MASS\_CANCEL\_REQUEST<br />29 = ORIGORDMODTIME<br />30 = DUPLICATE\_CLORDID<br />31 = PRICE\_EXCEEDS\_CURRENT\_PRICE |
| 58  | Text         | string | N        | Value may be forwarded from Coinbase Exchange                                                                                                                                                                                                                |

###### PreFillReport (35=F8)

Not sent for spot orders routed to Coinbase Exchange.

##### FIX API, Market Data

For spot instruments configured to route spot orders to Coinbase Exchange, all values represent the unless otherwise noted,

###### SecurityList (35=y) & SecurityDefinition (35=d)

The following only applies for spot instruments configured to route spot orders to Coinbase Exchange.

| Tag  | Name                    | Type | Required | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| :--- | :---------------------- | :--- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 871  | InstrAttribType         | int  | Y        | The following values are not sent:<br /><br />40 = Average daily notional amount<br />42 = Total day notional amount (30 days)<br />44 = Total hour notional amount (24 hours)<br /><br />Other values are forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1682 | MDSecurityTradingStatus | int  | Y        | New values include:<br /><br />100 = AUCTION\_MODE<br />101 = CANCEL\_ONLY<br />102 = POST\_ONLY<br />103 = LIMIT\_ONLY<br />104 = TRADING\_DISABLED<br />105 = CANCEL\_ONLY\_ENFORCED\_BY\_COINBASE\_INTERNATIONAL\_EXCHANGE<br />106 = COINBASE\_EXCHANGE\_UNREACHABLE<br /><br />All new options, except for the following, are forwarded from Coinbase Exchange. `CANCEL_ONLY_ENFORCED_BY_COINBASE_INTERNATIONAL_EXCHANGE` means Coinbase International Exchange only permits order cancellation separately from Coinbase Exchange. `COINBASE_EXCHANGE_UNREACHABLE` means the Coinbase International Exchange component is unable to establish connectivity with Coinbase Exchange |

###### MarketDataSnapshotFullRefresh (35=W) & MarketDataIncrementalRefresh (35=X)

The following only applies for spot instruments configured to route spot orders to Coinbase Exchange.

| Tag  | Name          | Type | Required | Notes                                                                                                                                                                                    |
| :--- | :------------ | :--- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 269  | MDEntryType   | char | Y        | The following values are not sent:<br /><br />4 = Opening price<br />g = Fair value limit up<br />h = Fair value limit down<br /><br />Other values are forwarded from Coinbase Exchange |
| 2446 | AggressorSide | int  | C        | Forwarded from Coinbase Exchange                                                                                                                                                         |

##### WebSocket Feed

###### INSTRUMENTS Channel

The following only applies for spot instruments configured to route spot orders to Coinbase Exchange.

*Response*

| Property                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| trading\_state            | New available options include: `auction_mode`, `cancel_only`, `post_only`, `limit_only`, `trading_disabled`, `cancel_only_enforced_by_coinbase_international_exchange`, `coinbase_exchange_unreachable`<br /><br />All new options, except for the following, are forwarded from Coinbase Exchange. `cancel_only_enforced_by_coinbase_international_exchange` means Coinbase International Exchange only permits order cancellation separately from Coinbase Exchange. `coinbase_exchange_unreachable` means the Coinbase International Exchange component is unable to establish connectivity with Coinbase Exchange |
| avg\_daily\_quantity      | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| total\_30\_day\_quantity  | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| total\_24\_hour\_quantity | Forwarded from Coinbase Exchange                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| avg\_daily\_volume        | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| total\_30\_day\_volume    | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| total\_24\_hour\_volume   | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| indicative\_open\_price   | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| min\_quantity             | Will not be populated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

###### CANDLES Channel

Not supported for spot instruments configured to route orders to Coinbase Exchange.

### 2025-OCT-23

#### Instrument Definition Updates

* **REST API**
  * Added `min_quantity` field to response from [List Instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [Get Instrument Details](/api-reference/international-exchange-api/rest-api/instruments/get-instrument-details) endpoints

### 2025-OCT-16

#### Address Book

* **REST API**
  * New [Get Address Book](/api-reference/international-exchange-api/rest-api/address-book/get-address-book) endpoint to retrieve all saved withdrawal recipients

### 2025-AUG-14

Users can now query position transfers with the new transfer type `POSITION_TRANSFER`.

* **REST API**
  * New transfer type in [Get Transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) endpoint:
    * New supported type: `POSITION_TRANSFER`

### 2025-AUG-06

Adding two new fields for external collateral users.

* **REST API**
  * New fields `unreconciled_amount` and `max_undelegate_amount` for
    * [Get Balance For Portfolio/Asset](/api-reference/international-exchange-api/rest-api/portfolios/get-balance-for-assests)
    * [List Portfolio Balance](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-balances)
    * [Get Portfolio Details](/api-reference/international-exchange-api/rest-api/portfolios/get-portfolio-details)

### 2025-JUN-23

#### Two-Sided Position Limits

Introducing two-sided position limits for perpetual futures position limit accounting.

In this model, long position notional and short position notional values are tracked separately, and the maximum value across the account is the effective value when determining limit breach

* **REST API**
  * New values in Position response for [Get Portfolio Position](/api-reference/international-exchange-api/rest-api/portfolios/get-position-portfolio) and [List Portfolio Positions](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-positions):
    * `open_position_notional`: max(long\_open\_position\_notional, short\_open\_position\_notional)
    * `long_open_position_notional`
    * `short_open_position_notional`

#### Disable Loan Overdraft Protection on a Portfolio

We are adding support to disable loan overdraft protection on a per-portfolio basis.
Overdraft loans will not be issued during settlement or any loan acquisition processes that are not initiated by the user.

* **REST API**
  * New parameter to enable/disable overdraft protection to [Portfolio Patch](/api-reference/international-exchange-api/rest-api/portfolios/patch-portfolio) endpoint:
    * `disable_overdraft_protection`

### 2025-APR-24

#### Margin Call

Introducing margin call functionality for underwritten clients.

* **REST API**
  * New [margin call status endpoint](/api-reference/international-exchange-api/rest-api/portfolios/get-portfolio-margin-call) to get margin call status for a portfolio
  * New parameter, `marginCallEnabled`, to enable/disable margin call to [portfolio patch endpoint](/api-reference/international-exchange-api/rest-api/portfolios/patch-portfolio)
  * Added `destination_tag` to the [Withdraw to crypto address](/api-reference/international-exchange-api/rest-api/transfers/withdraw-to-crypto-address) endpoint to support transfers for additional assets

#### TP/SL Order Replace

Added support for replacing [TP/SL orders](/international-exchange/fix-api/tpsl-orders#order-replace):

* **FIX API**

  * Added a new field **StopLimitPx** (tag 3040) to the [OrderCancelReplaceRequest (35=G)](/international-exchange/fix-api/order-entry-messages#ordercancelreplacerequest-35g) message.
  * Updated the FIX dictionary [download link](/international-exchange/fix-api/dictionary-downloads)

* **REST API**
  * Added a new filed `stop_limit_price` to the [Modify order](/api-reference/international-exchange-api/rest-api/orders/modify-open-order#body-stop-limit-price) in the REST API.

#### Higher FIX API Key-level Rate Limits

We have increased FIX API key-level rate limits:

* Increase FIX messages per second per API key from 400 to 800.
* Increase FIX disconnect threshold messages per second per API key from 700 to 1000.

### 2025-MAR-27

* **FIX API**
  Added new FIX messages for Request For Quote (RFQ). The new FIX messages are:
  * [RFQRequest](/international-exchange/fix-api/order-entry-messages#rfq-request-35ah)
  * [QuoteRequest](/international-exchange/fix-api/order-entry-messages#quote-request-35r)
  * [Quote](/international-exchange/fix-api/order-entry-messages#quote-35s)
  * [QuoteStatusReport](/international-exchange/fix-api/order-entry-messages#quote-status-report-35ai)
* **WebSockets**
  * Added the [RFQ MATCH channel](/international-exchange/websocket-feed/channels#rfq-match-channel) to provide real-time information every time an RFQ trade happens.
* **REST API**
  * [Get Instrument Details](/api-reference/international-exchange-api/rest-api/instruments/get-instrument-details) and [List Instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) endpoints
    * Add new field to indicate fee rate charged for rfq quotes: `rfq_maker_fee_rate`
  * [Get Portfolio Fills](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills) and [List Portfolio Fills](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills) endpoints
    * Add new field to indicate execution venue: `execution_venue` \[`RFQ`, `CLOB`]

### 2025-MAR-13

Introducing 2 new endpoints to get portfolio transfer limits.

* **REST API**
  * [Get transfer limit between portfolios](/api-reference/international-exchange-api/rest-api/portfolios/get-fund-transfer-limit)
  * [Get counterparty withdrawal limit](/api-reference/international-exchange-api/rest-api/transfers/get-counterparty-withdrawal-limit)
  * The existing [Counterparty transfer](/api-reference/international-exchange-api/rest-api/transfers/withdraw-to-counterparty-id) endpoint now supports transfer of borrowed funds.

### 2025-FEB-27

Added transfer activity to the Get Transfers endpoint representing automatic portfolio to portfolio balance transfers made to cover losses during liquidation.

* **REST API**
  * Added new transfer activity to the [Get Transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) endpoint
    * New supported types: `LIQUIDATION_EQUITY_CLAWBACK`

### 2025-FEB-13

Introducing 3 new endpoints to get portfolio open position notional limits.

* **REST API**
  * [Get the total open position limit for the portfolio](/api-reference/international-exchange-api/rest-api/portfolios/get-the-total-open-position-limits)
  * [List the open position limits for all instruments](/api-reference/international-exchange-api/rest-api/portfolios/get-the-open-position-limits)
  * [Get the open position limits for the portfolio instrument](/api-reference/international-exchange-api/rest-api/portfolios/get-the-open-position-limits)

Adding Real Time Settlement Transfer events to the Get Transfers endpoint.

* **REST API**
  * Add real time settlement transfers to the [Get Transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) endpoint
    * New supported types: `REAL_TIME_SETTLEMENT`

### 2025-FEB-06

#### Session CancelOnDisconnect Default Behavior

The default value for both CancelOrdersOnDisconnect and CancelOrdersOnInternalDisconnect in the [FIX Logon](/international-exchange/fix-api/admin-messages#logon-35a) message changed from `N` (No cancel on disconnect) to `Y` (Only cancels orders from this session).

**CancelOrdersOnDisconnect (Tag 8013)**

* **Old Default**: `N` (No cancel on disconnect)
* **New Default**: `Y` (Only cancels orders from this session)

**CancelOrdersOnInternalDisconnect (Tag 8014)**

* **Old Default**: `N` (No cancel on internal disconnect)
* **New Default**: `Y` (Only cancels orders from this session)

### 2025-JAN-16

Replacing quantity risk limits with notional ones:

* **REST API**
  * `position_notional_limit` and `open_interest_notional_limit` to the [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) response objects.
* **FIX API**
  * New `PositionLimit` field (tag 970) in Market Data. This a new field is on the [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) message
  * The field `MaxTradeVol` will be deprecated in the future changes.
* Order rejection uses `UBO_HIGH_LEVERAGE_NOTIONAL_BREACHED` instead of `UBO_HIGH_LEVERAGE_QUANTITY_BREACHED`.
* Updated the FIX dictionary [download link](/international-exchange/fix-api/dictionary-downloads)

Adding new instrument trading state `EXTERNAL`:

* **EXTERNAL Trading State**

  * Instruments that have an `EXTERNAL` trading status are not currently traded on this market. This is used to derive collateral value of instruments that does not have a quoted USDC price.

* **REST API**
  * Added `trading_state` value `EXTERNAL` to the [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) response objects.

* **FIX API**
  * Added MdSecurityTradingStatus (Tag 1682) value 19 (Not Traded On This Market) to [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) and [SecurityList](/international-exchange/fix-api/market-data#securitylist-35y) messages

* **WEB MD API**
  * Added `trading_state` value `external` to the [INSTRUMENTS Channel](/international-exchange/websocket-feed/channels#instruments-channel) response.
  * WEB MD API will not subscribe to MDA candles data for `external` instruments
  * WEB MD API will reject client subscription requests to all channels except `RISK` and `INSTRUMENT` for `external` instruments

* Updated <a href={`/international-exchange/downloads/cb_intx_fix_dictionaries_latest.tar.gz`}>cb\_intx\_fix\_dictionaries\_latest.tar.gz</a>
  for download

### 2024-DEC-18

* **REST API**
  * Populated `txn_hash` for both on-chain deposits and on-chain withdrawals in the responses for [Get transfer](/api-reference/international-exchange-api/rest-api/transfers/get-transfer) and [Get transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers).

### 2024-DEC-13

* **REST API**
  * Added `instrument_symbol` and `txn_hash` field to the responses for [Get transfer](/api-reference/international-exchange-api/rest-api/transfers/get-transfer) and [Get transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) respectively.
    * `txn_hash` will be present for on-chain deposit transfers
    * `instrument_symbol` will be present for funding transfers

### 2024-NOV-25

Added support for Exchange Loans

* **REST API**
  * Added [Update Loan](/api-reference/international-exchange-api/rest-api/portfolios/acquire-and-repay-loan) endpoint to acquire/repay existing loans
  * Added [Preview Loan](/api-reference/international-exchange-api/rest-api/portfolios/preview-loan-update) endpoint to preview the portfolio state after acquiring a loan
  * Added [Loan Availability](/api-reference/international-exchange-api/rest-api/portfolios/view-max-loan) endpoint to retrieve the maximum loan amount available for the specified asset
  * Added [Get Portfolio Loans](/api-reference/international-exchange-api/rest-api/portfolios/list-active-loans-for-the-portfolio) endpoint to view all loans for a portfolio
  * Added [Get Portfolio Loan](/api-reference/international-exchange-api/rest-api/portfolios/get-loan-info-for-portfolio) endpoint to view the existing loan state for the specified asset
  * Changes to fields in the [Balance](/api-reference/international-exchange-api/rest-api/portfolios/get-balance-for-assests) response object
    * Added `collateral_backed_overdraft_loan` amount (quantity) of outstanding loan taken due to overdrafting USDC on a debit
    * Added `user_requested_loan` amount (quantity) of outstanding loan requested by the user
    * Changed `loan` to be the total loan amount (quantity) outstanding. Sum of `collateral_backed_overdraft_loan` and `user_requested_loan`
    * Added `loan_initial_margin_contribution` the amount of initial margin required to hold the existing loan
  * Changes to the fields in the [Asset](/api-reference/international-exchange-api/rest-api/assets/list-assets) response object
    * Added `loan_initial_margin` the percentage of initial margin requirement for taking a loan on the asset
    * Added `max_loan_leverage` the maximum amount leverage that can be used when taking a loan on the asset
  * Added loan activity to the [Get Transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) endpoint
    * New supported types: `LOAN_ACQUIRE`, `LOAN_REPAY`, `LOAN_INTEREST_CHARGE`, and `ALL_LOANS`
    * The `ALL_LOANS` type will include all transfers related to acquire, repay, and interest charge activity

### 2024-NOV-21

Added new text field to denote cancel reason in [get order](/api-reference/international-exchange-api/rest-api/orders/list-open-orders) endpoint

### 2024-NOV-12

Added new REST API endpoints for retrieving index data:

* [Get index composition](/api-reference/international-exchange-api/rest-api/index/get-index-composition)
* [Get index composition history](/api-reference/international-exchange-api/rest-api/index/get-index-composition-history)
* [Get index price](/api-reference/international-exchange-api/rest-api/index/get-index-price)
* [Get index candles](/api-reference/international-exchange-api/rest-api/index/get-index-candles)

### 2024-OCT-24

API changes for TWAP orders:

* **FIX API**
  * Added `TargetStrategy (Tag 847)` to [NewOrderSingle](/international-exchange/fix-api/order-entry-messages#newordersingle-35d) and [ExecutionReport](/international-exchange/fix-api/order-entry-messages#executionreport-358) messages
* **REST API**
  * Added `algo_strategy` to the [Create order](/api-reference/international-exchange-api/rest-api/orders/create-order) request object and its response

### 2024-SEP-12

Adding new FIX field to instrument definition:

* **FIX API**
  * Added `NoUnderlyings (Tag 711)` to [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) and [SecurityList](/international-exchange/fix-api/market-data#securitylist-35y) messages

### 2024-SEP-10

Added new instrument trading state `DELISTED`:

* **REST API**
  * Added `trading_state` value `DELISTED` to the [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) response objects.
* **FIX API**
  * Added `MdSecurityTradingStatus (Tag 1682)` value `18 (Not Available to Trade)` to [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) and [SecurityList](/international-exchange/fix-api/market-data#securitylist-35y) messages
* **WEB MD API**
  * Added `trading_state` value `delisted` to the [INSTRUMENTS Channel](/international-exchange/websocket-feed/channels#instruments-channel) response

### 2024-SEP-03

Adding new FIX messages for the PreFills API. The new FIX messages are:

* [PreFillRequest](/international-exchange/fix-api/order-entry-messages#prefillrequest-35f6)
* [PreFillReport](/international-exchange/fix-api/order-entry-messages#prefillreport-35f8)

### 2024-AUG-20

Adding new field `underlying_type` which represents the underlying asset type. The enhanced REST API endpoints are:

* [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments)
* [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/list-instruments)

### 2024-JUL-30

Renamed `fill_source` to `source` in REST API endpoints:

* [List portfolio fills](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills)
* [List fills by portfolios](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills)

### 2024-JUL-22

Added `fill_source` (LIQUIDATION, CLIENT\_ORDER) to REST API endpoints:

* [List portfolio fills](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills)
* [List fills by portfolios](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills)

### 2024-JUL-11

Updated and added [rate limits](/international-exchange/introduction/rate-limits-overview):

* Updated REST requests per second per API Key from 100 to 40
* Updated Maximum API Keys per account to:
  * Maximum **trading** API Keys per account: 30
  * Maximum **non-trading** API Keys per account: 20
* Added Maximum connection attempts every 30 seconds: 10

### 2024-JUN-17

Added support for Pre-Launch Markets. Pre-Launch Markets let users trade perpetual futures contracts on tokens that have not launched yet. When an underlying token is launched on an applicable spot exchange, the instrument converts to a standard perpetual contract. Learn more in our [Help Center](https://help.coinbase.com/en/international-exchange/pre-launch-markets/what-is-a-pre-launch-market).

* **REST API**
  * Added `mode` (STANDARD, PRE\_LAUNCH, PRE\_LAUNCH\_CONVERTING) to the [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) response objects.
  * Added `pre_launch_trading_enabled` to the [Patch portfolio](/api-reference/international-exchange-api/rest-api/portfolios/patch-portfolio) request and [Get user portfolio](/api-reference/international-exchange-api/rest-api/portfolios/get-user-portfolio) response objects.
* **FIX API**
  * Added `SecuritySubType (Tag 762)` (STANDARD, PRE\_LAUNCH, PRE\_LAUNCH\_CONVERTING) to [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) and [SecurityList](/international-exchange/fix-api/market-data#securitylist-35y) messages
  * Added repeating group `NoEvents (864)` under the Instrument Component in the [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) and [SecurityList](/international-exchange/fix-api/market-data#securitylist-35y) messages
  * Updated the FIX dictionary [download link](/international-exchange/fix-api/dictionary-downloads)
* **WEB MD API**
  * Added `instrument_mode` (standard, pre\_launch, pre\_launch\_converting) and `pre_launch_conversion_time` to the [INSTRUMENTS Channel](/international-exchange/websocket-feed/channels#instruments-channel) response

### 2024-JUN-06

* **WebSockets**
  * Added the [CANDLES channels](/international-exchange/websocket-feed/channels#candles-channels) for market data.

### 2024-MAY-23

* **REST API**
  * Added [List position offsets](/api-reference/international-exchange-api/rest-api/position-offsets/list-position-offsets) REST endpoint
  * Added `close_only` field to the [Create order](/api-reference/international-exchange-api/rest-api/orders/create-order) request object.
  * Added `close_only` field to the [Get order details](/api-reference/international-exchange-api/rest-api/orders/get-order-details) and [List open orders](/api-reference/international-exchange-api/rest-api/orders/list-open-orders) response objects.
  * Added `base_asset_multiplier` field to the [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) response objects.
* **FIX API**
  * Added `CLOSE_ONLY` to the supported `ExecInst` values of the [NewOrderSingle](/international-exchange/fix-api/order-entry-messages#newordersingle-35d) and [ExecutionReport](/international-exchange/fix-api/order-entry-messages#executionreport-358) messages in the order entry fix dictionary.
  * Added `CLOSE_ONLY` to the supported `ExecInst` values of the [ExecutionReport](/international-exchange/fix-api/order-entry-messages#executionreport-358) message in the drop copy fix dictionary.
  * Added `ContractMultiplier (Tag 231)` to [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) and [SecurityList](/international-exchange/fix-api/market-data#securitylist-35y) messages
  * Updated the FIX dictionary [download link](/international-exchange/fix-api/dictionary-downloads)
* **WEB MD API**
  * Added `base_asset_multiplier` to the [INSTRUMENTS Channel](/international-exchange/websocket-feed/channels#instruments-channel) response

### 2024-MAY-13

* Added [Patch portfolio](/api-reference/international-exchange-api/rest-api/portfolios/patch-portfolio) REST endpoint

### 2024-MAY-02

* Added the `order_type` and `side` parameters to [List open orders](/api-reference/international-exchange-api/rest-api/orders/list-open-orders) REST endpoint

### 2024-APR-25

Added the following REST endpoints:

* [Get daily trading volumes](/api-reference/international-exchange-api/rest-api/instruments/get-daily-trading-volume)
* [Get aggregated candles data per instrument](/api-reference/international-exchange-api/rest-api/instruments/get-aggegated-candles)

### 2024-APR-17

Added portfolio Auto Margin:

* Portfolios automatically post the collateral required to exceed high leverage limits on a per-instrument basis.
* Portfolio margin requirements are calculated based on the newly introduced default initial margin instrument field.
* Users can opt-in to the Auto Margin feature on a per-portfolio basis.

#### Instrument Definitions

Added the following instrument definitions for Auto Margin:

* `default_imf` to [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments)
* `default_imf` to the WebSocket [INSTRUMENTS Channel](/international-exchange/websocket-feed/channels#instruments-channel)
* `DefaultMarginRatio` to the FIX API Market Data [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) message
* Updated the FIX dictionary [download link](/international-exchange/fix-api/dictionary-downloads)

#### Portfolio Endpoints

* Added an endpoint to [Enable/Disable portfolio auto margin](/api-reference/international-exchange-api/rest-api/portfolios/enable-and-disable-portfolio)

### 2024-APR-02

Updated REST and FIX API to support TP/SL orders:

* Added new field `stop_limit_price` and new option `TAKE_PROFIT_STOP_LOSS` for field `order_type` on the REST API [order create](/api-reference/international-exchange-api/rest-api/orders/create-order), [order details](/api-reference/international-exchange-api/rest-api/orders/get-order-details) and [order list](/api-reference/international-exchange-api/rest-api/orders/list-open-orders)
* Added new field `StopLimitPx` (tag `3040`) and new option `O` for field `OrderType` on the FIX Order Entry API [NewOrderSingle](/international-exchange/fix-api/order-entry-messages#newordersingle-35d) and [ExecutionReport](/international-exchange/fix-api/order-entry-messages#executionreport-358) messages

### 2024-MAR-27

Added support for portfolio cross collateral:

* Added opt-in endpoint, [Enable/Disable portfolio cross collateral](/api-reference/international-exchange-api/rest-api/portfolios/enable-and-disable-cross)
* Updated the responses for the following APIs with loan and collateral information:
  * [List portfolio balances](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-balances)
  * [Get portfolio details](/api-reference/international-exchange-api/rest-api/portfolios/get-portfolio-details)
  * [Get asset details](/api-reference/international-exchange-api/rest-api/assets/get-asset-details)
  * [List assets](/api-reference/international-exchange-api/rest-api/assets/list-assets)

### 2024-MAR-26

Added new REST API for position transfer -- requires `trade` permission:

* [Transfer positions between portfolios](/api-reference/international-exchange-api/rest-api/portfolios/transfer-positions)

### 2024-MAR-19

Added new REST APIs for fee rate tiers:

* [List fee rate tiers](/api-reference/international-exchange-api/rest-api/fee-rates/list-fee-rate-tiers)
* [List portfolio fee rates](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fee-rates)

### 2024-FEB-27

* Added [OrderMassCancelRequest](/international-exchange/fix-api/order-entry-messages#ordermasscancelrequest-35q) and [OrderMassCancelReport](/international-exchange/fix-api/order-entry-messages#ordermasscancelreport-35r) messages to the FIX Order Entry API
* Added the `side` parameter to the [Cancel Orders](/api-reference/international-exchange-api/rest-api/orders/cancel-orders) REST endpoint for bulk order cancels

### 2024-FEB-22

* Made the <a href={`/api-reference/international-exchange-api/rest-api/intx-spec.yaml`}>International Exchange OpenAPI Specification</a> available for download.

### 2024-FEB-06

* Increased [Maximum API keys per account](/international-exchange/introduction/rate-limits-overview#general-maximums) to 20.

### 2024-JAN-30

* Added `id` field to portfolio position related endpoints to denote position ID.
* Exposed `position_id` on transfers of type `FUNDING` to the [Get transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) response.
* Added new `hold_available_for_collateral` field to [Get portfolio details](/api-reference/international-exchange-api/rest-api/portfolios/get-portfolio-details), [Get balance for portfolio/asset](/api-reference/international-exchange-api/rest-api/portfolios/get-balance-for-assests), and [List portfolio balances](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-balances) REST endpoints.

### 2024-JAN-23

* Added `instrument_id` field to the responses for [Get transfer](/api-reference/international-exchange-api/rest-api/transfers/get-transfer) and [Get transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) for transfers of type `FUNDING`

### 2024-JAN-15

* Added new transfer endpoints:
  * [Create counterparty id](/api-reference/international-exchange-api/rest-api/transfers/create-counterparty-id)
  * [Validate a counterparty id](/api-reference/international-exchange-api/rest-api/transfers/validate-counterparty-id)
  * [Withdraw to a counterparty id](/api-reference/international-exchange-api/rest-api/transfers/withdraw-to-counterparty-id)
* Added `from_counterparty_id` and `to_counterparty_id` to [List matching transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) and [Get transfer](/api-reference/international-exchange-api/rest-api/transfers/get-transfer) REST endpoints.

### 2024-JAN-11

* Added new instrument endpoint: [Get historical funding rates](/api-reference/international-exchange-api/rest-api/instruments/get-historical-funding-rate)
* Added new transfer type `FUNDING` to Transfer related endpoints

### 2023-DEC-13

* Added fields from response of [`/instruments/{instrument}/quote`](/api-reference/international-exchange-api/rest-api/instruments/get-quote-per-instrument), as a `quote` object, to the responses of [`/instruments`](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) and [`/instruments/{instrument}`](/api-reference/international-exchange-api/rest-api/instruments/list-instruments).

### 2023-DEC-12

* Added `aggressor_side`to web market data [MATCH Channel](/international-exchange/websocket-feed/channels#match-channel).

* Replaced old return type with `portfolio_id` and `margin_override` fields in portfolio endpoint: [Set portfolio margin override](/api-reference/international-exchange-api/rest-api/portfolios/set-profile-margin)

### 2023-DEC-05

* Added guidance on FIX and REST API [Rate Limits](/international-exchange/introduction/rate-limits-overview).

### 2023-NOV-28

* Added `portfolio_initial_margin_notional`, `portfolio_current_margin_notional`, `portfolio_maintenance_margin_notional` and `portfolio_close_out_margin_notional` to Get portfolio summary and Get portfolio details REST endpoints.

### 2023-NOV-27

* Added new portfolio endpoint: [Set portfolio margin override](/api-reference/international-exchange-api/rest-api/portfolios/set-profile-margin)
* Updated description of MaxTradeVol in FIX [SecurityList](/international-exchange/fix-api/market-data#securitylist-35y) and [SecurityDefinition](/international-exchange/fix-api/market-data#securitydefinition-35d) messages.
* Updated response comment descriptions for [WebSockets INSTRUMENTS Channel](/international-exchange/websocket-feed/channels#instruments-channel)

### 2023-NOV-24

* Added **Cancel resting order** option (`8000=O`) to SelfTradePreventionStrategy tag:
  * [Trading NewOrderSingle (35=D) ](/international-exchange/fix-api/order-entry-messages#newordersingle-35d)
  * [Trading ExecutionReport (35=8) ](/international-exchange/fix-api/order-entry-messages#executionreport-358)

### 2023-NOV-09

* Added **Decrement and cancel resting order** option (`8000=D`) to SelfTradePreventionStrategy tag
  * [Drop Copy ExecutionReport (35=8)](/international-exchange/fix-api/drop-copy#executionreport-358)

### 2023-NOV-08

* Added `portfolio_maintenance_margin` and `portfolio_close_out_margin` to [Get portfolio summary](/api-reference/international-exchange-api/rest-api/portfolios/get-portfolio-details) and [Get portfolio details](/api-reference/international-exchange-api/rest-api/portfolios/get-portfolio-details) REST endpoints.

### 2023-OCT-30

* Added new portfolio endpoints:

  * [Get portfolio](/api-reference/international-exchange-api/rest-api/portfolios/get-user-portfolio)
  * [Create portfolio](/api-reference/international-exchange-api/rest-api/portfolios/create-portfolio)
  * [Update portfolio](/api-reference/international-exchange-api/rest-api/portfolios/update-portfolio)
  * [List fills by portfolios](/api-reference/international-exchange-api/rest-api/portfolios/list-fills-portfolio)
  * [Transfer funds between portfolios](/api-reference/international-exchange-api/rest-api/portfolios/transfer-funds) (requires `transfer` permission)

* Added ability to query transfers by multiple portfolios:
  * [Get transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers)

### 2023-OCT-19

* Updated the field type of `LastUpdateTime` from `UTCDATEONLY` to `UTCTIMESTAMP` in `SecurityDefinition` in [FIX50 Market Data Dictionary](/international-exchange/fix-api/dictionary-downloads)

### 2023-OCT-18

* Added `open_interest` to [WebSocket feed](/international-exchange/websocket-feed/channels#risk-channel), [FIX Market Data API](/international-exchange/fix-api/market-data#marketdatasnapshotfullrefresh-35w), and [REST API](/api-reference/international-exchange-api/rest-api/instruments/list-instruments).

### 2023-SEP-28

* Added new endpoint `/transfers/withdraw`: [Withdraw to crypto address](/api-reference/international-exchange-api/rest-api/transfers/withdraw-to-crypto-address)
* Multi-chain support for USDC transfers on Base/Optimism networks

### 2023-JUL-21

* Added support for multi-chain/gasless transfers. Users are now able to deposit and withdraw USDC on Arbitrum, Avalanche, Ethereum, Polygon, and Solana networks.
* Added 24h/30d volume figures to
  * [FIX MarketData SecurityList](/international-exchange/fix-api/market-data#securitylist-35y)
  * [FIX MarketData SecurityDefinition](/international-exchange/fix-api/market-data)
  * [WebSocket Instruments Channel](/international-exchange/websocket-feed/channels#instruments-channel)
* Improved REST API latency
* Updated the INTX UI with a new Transfers History page and 24h/30d volume figures

### 2023-JUL-11

* Added [tarball of FIX dictionaries](/international-exchange/fix-api/dictionary-downloads) for download.

### 2023-JUN-01

##### WebSocket

* Added [WebSocket Market Data API](/international-exchange/websocket-feed/websocket-overview)

##### REST API

* Added new endpoint `/transfers`:
  * [List matching transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers)
  * [Get transfer](/api-reference/international-exchange-api/rest-api/transfers/get-transfer)
  * [Create crypto address](/api-reference/international-exchange-api/rest-api/transfers/create-crypto-address)
* Added ability to filter on a specific `order_id` for `fills` endpoint:
  * [List portfolio fills](/api-reference/international-exchange-api/rest-api/portfolios/list-portfolio-fills)

##### INTX UI

* Publish 24h volume on Markets page
* Fixed issue displaying "Short" positions

### 2023-MAY-19

Improved overall system performance and stability. Features include:

* 20 new price levels on the [FIX Market Data feed](/international-exchange/fix-api/market-data).
* Reduced latency of the [REST API `orders`](/api-reference/international-exchange-api/rest-api/orders/create-order) endpoint.
* Ability to fetch [REST API `orders`](/api-reference/international-exchange-api/rest-api/orders/create-order) under the same portfolio.

### 2023-MAY-02

* Public preview of the Coinbase International Exchange FIX and REST APIS.

