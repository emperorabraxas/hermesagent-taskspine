# INTX Changelog
Source: https://docs.cdp.coinbase.com/international-exchange/changes/changelog



These release notes list changes to all Coinbase International Exchange products.

### 2026-Mar-19

#### Underlying Security Type

Introducing new underlying security type values which may be sent in instrument definition messages across REST, WebSocket, and FIX Market Data APIs. WebSocket and FIX Market Data APIs will also begin publishing `underlying_type` and `UnderlyingSecurityType` (Tag 310).

##### REST API, WebSocket Feed

The following new values may now be sent in the `underlying_type` field:

| Value         | Description                                     |
| :------------ | :---------------------------------------------- |
| EQUITY        | Contract based on equity single stock           |
| EQUITY\_ETF   | Contract based on equity ETF                    |
| EQUITY\_INDEX | Contract based on equity custom basket or index |

The above field is sent in:

1. REST API's [List instruments](/api-reference/international-exchange-api/rest-api/instruments/list-instruments) endpoint
2. REST API's [Get instrument details](/api-reference/international-exchange-api/rest-api/instruments/get-instrument-details) endpoint
3. WebSocket Feed's `INSTRUMENTS` Channel

##### FIX API, Market Data

###### SecurityDefinition (35=d) & SecurityList (35=y)

The following new values may now be sent in `UnderlyingSecurityType` (Tag 310):

| Tag | Name                   | Type   | Required | Values                                                                                                                                                                                  |
| :-- | :--------------------- | :----- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 310 | UnderlyingSecurityType | STRING | N        | `EQUITY` = CONTRACT\_BASED\_ON\_EQUITY\_SINGLE\_STOCK<br />`EQUITY_ETF` = CONTRACT\_BASED\_ON\_EQUITY\_ETF<br />`EQUITY_INDEX` = CONTRACT\_BASED\_ON\_EQUITY\_CUSTOM\_BASKET\_OR\_INDEX |

### 2026-FEB-19

#### FIX Market Data: `MarketDataIncrementalRefresh` `MDEntry`'s where `MDEntryType=BID|OFFER`: New `LastFragment` and `MDEntryTime` fields

Two new fields will be added to `MarketDataIncrementalRefresh` messages which contain `MDEntry`(s) (repeating group component whose count is published as `NoMDEntries/268`) whose `MDEntryType/269` is `BID/0` or `ASK/1`. <u>This does not require clients to modify their FIX engine behavior</u> as both fields merely add additional metadata without any change to the underlying data sent.

1. `LastFragment/893`
   * `BOOLEAN` type. Not required. Either set to `YES/Y` or not populated. Set on `MarketDataIncrementalRefresh` itself rather than in `MDEntry` components.
   * If set to `YES/Y`, the `MDEntry`s in the message are the final updates in a batch (please see the *`MDEntryType=BID|OFFER` Batch Fragmentation* sub-section below).

2. `MDEntryTime/273`
   * `UTCTIMESTAMP` type. Not required. Only and always set on `MDEntry`s components where `MDEntryType=BID|OFFER`. Millisecond precision.
   * Contains the time the order event which triggered the price level change occurred. This time is different from `TransactTime/60`, which contains a time equal *or higher* than the order event time.

##### `MDEntryType=BID|OFFER` Batch Fragmentation

`MarketDataIncrementalRefresh` messages containing these `MDEntryType`s for L2 data (all price levels) batch price level updates for performance reasons, meaning multiple price level updates are queued together before they are sent together in a batch. To prevent any single `MarketDataIncrementalRefresh` from becoming to large, a batch may be sent in multiple `MarketDataIncrementalRefresh`s ("fragments").

Clients may queue (but not process) `MDEntryType=BID|OFFER`s for `MarketDataIncrementalRefresh`s without `LastFragment` populated. On receipt of a `MarketDataIncrementalRefresh` with `LastFragment=Y`, clients may then queue the included `MDEntryType=BID|OFFER`s and then process all queued `MDEntryType=BID|OFFER`s for the `Symbol` which all the included `MDEntry`s are set to. This permits clients to process batches altogether at once rather than individual updates.

### 2026-Jan-22

#### Position Transfer Metadata

We are adding a new `position_price` field to the [Get transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) and [Get transfer](/api-reference/international-exchange-api/rest-api/transfers/get-transfer) REST API endpoints to indicate the price at which a position transfer was made.

### 2025-DEC-19

#### Cursor-Based Pagination for Transfers

Added optional cursor-based pagination support to the [Get Transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) endpoint. This provides stable, consistent results when paginating through transfers, preventing duplicate results that can occur with offset-based pagination when new transfers are inserted between requests.

**When to use cursor vs offset pagination:**

* Use **cursor-based pagination** to avoid duplicate results when new transfers are created between paginated requests (though slightly slower than offset pagination)

* Use **offset-based pagination** for better performance when consistency across pages is not critical

* **REST API**
  * New optional query parameters for [Get Transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers):
    * `pagination_type`: Specifies pagination method (`OFFSET` or `CURSOR`)
    * `search_after_time`: Timestamp for cursor-based pagination
    * `search_after_idem`: Idempotency key for cursor-based pagination
  * New response fields in pagination object:
    * `search_after_time`: Echoes the timestamp used in the current request
    * `search_after_idem`: Echoes the idempotency key used in the current request

### 2025-NOV-20

#### Position Transfer Metadata

Adding position transfer metadata in the REST API [Get transfers](/api-reference/international-exchange-api/rest-api/transfers/list-matching-transfers) and [Get transfer](/api-reference/international-exchange-api/rest-api/transfers/get-transfer)
endpoints.

We are adding new fields `position_from_portfolio` and `position_to_portfolio` to denote the portfolios sending and receiving the transferred position.

A position transfer action generates two transfer events: one for the `position_from_portfolio` and one for the `position_to_portfolio`.
Both events share the same `position_transfer_reference_id`, which can be used to link them together.

The field `instrument_id` and `instrument_symbol` will show the transferred position instrument, and `position_size` and `position_side` will show the transferred position size and side.

The following is an example transfer returned from the above REST endpoints with explanation on the fields.

```