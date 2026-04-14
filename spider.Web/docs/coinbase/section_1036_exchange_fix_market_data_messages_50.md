# Exchange FIX Market Data Messages 5.0
Source: https://docs.cdp.coinbase.com/exchange/fix-api/market-data



The FIX market data API provides an L3 feed only with direct, low-latency, deterministic access.

About this API:

* **Baseline**: [FIX 5.0 SP2 specification](https://www.onixs.biz/fix-dictionary/5.0.sp2/index.html).
* **Environments**: Production, Sandbox

<Info>
  Environment URLs

  * Production Snapshot Enabled Gateway: `tcp+ssl://fix-md.exchange.coinbase.com:6121`
  * Production Snapshot Disabled Gateway: `tcp+ssl://fix-md.exchange.coinbase.com:6122`
  * Sandbox Snapshot Enabled Gateway: `tcp+ssl://fix-md.sandbox.exchange.coinbase.com:6121`
  * Sandbox Snapshot Disabled Gateway: `tcp+ssl://fix-md.sandbox.exchange.coinbase.com:6122`
</Info>

You can connect with the same authentication as our existing FIX order entry system. Connectivity is limited to a single connection per API key—Order Entry [rate limits](/exchange/fix-api/rate-limits) *do not apply* (connections, rps, burst rps).

<Warning>
  FIX5 Resets Saturdays at 1PM ET

  FIX5 Order Entry and Market Data customers will be logged out every Saturday at 1PM ET (6PM UTC).
</Warning>

## Header

A standard header must be present at the start of every message in both directions.

| Tag | FieldName    | Type         | Required | Notes                                                                         |
| :-- | :----------- | :----------- | :------- | :---------------------------------------------------------------------------- |
| 8   | BeginString  | String       | Y        | Must be `FIXT.1.1`                                                            |
| 49  | SenderCompID | String       | Y        | Client API key (on messages from the client)                                  |
| 56  | TargetCompID | String       | Y        | Must be `Coinbase` (on messages from client)                                  |
| 52  | SendingTime  | UTCTimestamp | Y        | UTC time down to millisecond resolution in the format `YYYYMMDD-HH:MM:SS.sss` |

## Logon (35=A)

| Tag  | FieldName        | Type    | Required | Notes                                                                           |
| :--- | :--------------- | :------ | :------- | :------------------------------------------------------------------------------ |
| 34   | MsgSeqNum        | Int     | Y        | Must be `1`                                                                     |
| 98   | EncryptMethod    | Int     | Y        | Must be `0` (None)                                                              |
| 108  | HeartBtInt       | Int     | Y        | Heartbeat interval is capped at 300s, defaults to 10s                           |
| 141  | ResetSeqNumFlag  | Boolean | Y        | Resets the sequence number. Can be `Y`/`N`                                      |
| 553  | Username         | String  | Y        | Client API Key                                                                  |
| 554  | Password         | String  | Y        | Client API passphrase                                                           |
| 95   | RawDataLength    | Int     | Y        | Number of bytes in RawData field                                                |
| 96   | RawData          | String  | Y        | [Client message signature](/exchange/rest-api/authentication#signing-a-message) |
| 1137 | DefaultApplVerID | String  | Y        | Must be `9` (FIX 5.0 SP2)                                                       |

## Market Data Request (35=V)

Clients should use this message to subscribe to or unsubscribe from market data for one or more symbols.

| Tag  | FieldName               | Type   | Required | Notes                                                                |
| :--- | :---------------------- | :----- | :------- | :------------------------------------------------------------------- |
| 262  | MDReqID                 | String | Y        | Client identifier for the market data request                        |
| 263  | SubscriptionRequestType | Int    | Y        | 1=Subscribe<br />2=Unsubscribe                                       |
| 146  | NoRelatedSym            | Int    | Y        | How many symbols are in the request                                  |
| =>55 | Symbol                  | String | Y        | Repeating group of symbols for which the client requests market data |

#### Market Data Request Reject (35=Y)

This message is sent to clients to reject an invalid market data request.

| Tag | FieldName      | Type   | Required | Notes                                                  |
| :-- | :------------- | :----- | :------- | :----------------------------------------------------- |
| 262 | MDReqID        | String | Y        | Client identifier for the market data request          |
| 281 | MDReqRejReason | Char   | Y        | 0=Unknown symbol<br />1=Duplicate MDReqID<br />7=Other |
| 58  | Text           | String | N        | Error description                                      |

## Security Status (35=f)

This message is streamed to clients together with the incremental updates for subscribed symbols and reflects changes in the trading status, tick size, or other attributes of an instrument.

| Tag   | FieldName               | Type    | Required | Notes                                                                                                                  |
| :---- | :---------------------- | :------ | :------- | :--------------------------------------------------------------------------------------------------------------------- |
| 262   | MDReqID                 | String  | Y        | Client identifier for the market data request                                                                          |
| 83    | RptSeq                  | Long    | Y        | Public sequence number by symbol                                                                                       |
| 55    | Symbol                  | String  | Y        | Repeating group of symbols for which the client requests market data                                                   |
| 1682  | MDSecurityTradingStatus | String  | Y        | `trading_disabled`<br />`cancel_only`<br />`post_only`<br />`limit_only`<br />`full_trading`<br />`auction_mode`<br /> |
| 969   | MinPriceIncrement       | Decimal | Y        | Minimum increment for quote currency (e.g., 0.01 USD for BTC-USD)                                                      |
| 29003 | MinSizeIncrement        | Decimal | Y        | Minimum increment for base currency (e.g., 0.00000001 BTC for BTC-USD)                                                 |

## Market Data Incremental Refresh (35=X)

Coinbase Exchange sends L3 order-by-order updates so clients can build a full book of all open orders, plus acknowledgements of orders by the matching engine with the order’s client order ID (ClOrdID) before matching. This helps clients immediately identify which orders and trades in the book (both aggressive and passive) are theirs, as well gain advance knowledge of orders that are pending processing by the matching engine. These acks correspond to the `Received` message in the web-socket feed.

* When `MDEntryID` is not present, the message is the acknowledgement of an order prior to matching.
* When `MDEntryID` is present, the message should be used for book-building. You can ignore Change messages with an MDEntryID for which you never received a New message.

<Info>
  When book-building, Change messages received before a corresponding New message can be ignored. Users may occasionally receive Change messages with `MDUpdateAction=1` and an MDEntryID with `Text=CHANGE_REASON_STP` when the quantity on the original received order was reduced due to Self-trade Prevention (prior to the order being placed on the order book).
</Info>

<Info>
  To maintain an up-to-date L3 order book when subscribing to the Snapshot Disabled Gateway:

  1. Send a `SubscriptionRequestType=1` Market Data Request (35=V) message for the product(s) of interest.
  2. Queue any Market Data Incremental Refresh (35=X) messages received over the FIX session.
  3. Make a [REST request](/api-reference/exchange-api/rest-api/products/get-product-book) for the order book snapshot from the REST API.
  4. Playback queued messages, discarding sequence numbers before or equal to the snapshot sequence number.
  5. Apply playback messages to the snapshot as needed.
  6. After playback is complete, apply real-time Market Data Incremental Refresh (35=X) messages as they arrive.
</Info>

| Tag     | FieldName      | Type         | Required | Notes                                                                                                                                                                                                                                                 |
| :------ | :------------- | :----------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 262     | MDReqID        | String       | Y        | Client identifier for the market data request                                                                                                                                                                                                         |
| 268     | NoMDEntries    | Int          | Y        | Always `1`                                                                                                                                                                                                                                            |
| =>279   | MDUpdateAction | Char         | Y        | 0=New<br />1=Change<br />2=Delete                                                                                                                                                                                                                     |
| =>269   | MDEntryType    | Char         | Y        | 0=Bid<br />1=Offer<br />2=Trade                                                                                                                                                                                                                       |
| =>278   | MDEntryID      | String       | N        | If present, this ID is the order ID that should be used for book-building<br />If not present, this message is the initial ack and should not be used to build the book                                                                               |
| =>83    | RptSeq         | Long         | Y        | Public sequence number by symbol                                                                                                                                                                                                                      |
| =>55    | Symbol         | String       | Y        | Repeating group of symbols for which the client requests market data                                                                                                                                                                                  |
| =>270   | MDEntryPx      | Decimal      | Y        | The price of the order                                                                                                                                                                                                                                |
| =>271   | MDEntrySize    | Decimal      | Y        | The quantity remaining of the order                                                                                                                                                                                                                   |
| =>60    | TransactTime   | UTCTimestamp | Y        | The engine timestamp of the order in microseconds                                                                                                                                                                                                     |
| =>40    | OrdType        | Char         | N        | Sent only if the message represents the initial ack of an order:<br />1=Market<br />2=Limit                                                                                                                                                           |
| =>11    | ClOrdID        | String       | N        | The client order ID on the initial ack of an order                                                                                                                                                                                                    |
| =>37    | OrderID        | String       | N        | The exchange order ID on the initial ack of an order<br />OR<br />If MDEntryType=2, then this is the aggressive Order ID                                                                                                                              |
| =>58    | Text           | String       | N        | If MDUpdateAction=1, then the possible values are:<br />`CHANGE_REASON_STP`<br />`CHANGE_REASON_MODIFY_ORDER`<br />`CHANGE_REASON_REMAINDER_AFTER_MODIFICATION`<br />If MDUpdateAction=2, then the possible values are:<br />`CANCELED`<br />`FILLED` |
| =>5797  | AggressorSide  | Int          | N        | Sent only on trades MDEntryType=2<br />1=Buy<br />2=Sell                                                                                                                                                                                              |
| =>29004 | Funds          | Decimal      | N        | Market orders may have an optional funds field which indicates how much quote currency is used to buy or sell                                                                                                                                         |

## Market Data Snapshot Full Refresh (35=W)

<Warning>
  Only Available On Snapshot Enabled Gateway

  The Market Data Snapshot Full Refresh (35=W) message is only supported on the Snapshot Enabled Gateway.
</Warning>

This message provides a full snapshot of all orders in the order book, including those placed before the client subscribed to incremental market data.

A snapshot is requested automatically when a successful Market Data Request from the client is processed for a given symbol. Clients should queue up incremental updates and process only the incremental updates with sequence number RptSeq greater than the RptSeq in the initial MD Snapshot Full Refresh snapshot message.

If clients are already subscribed to a symbol and send another Market Data Request to subscribe, they will not receive a new snapshot for that symbol. Clients must unsubscribe and subscribe to the market data again for a given symbol to receive a new snapshot.

| Tag   | FieldName               | Type    | Required | Notes                                                                                                            |
| :---- | :---------------------- | :------ | :------- | :--------------------------------------------------------------------------------------------------------------- |
| 262   | MDReqID                 | String  | Y        | Client identifier for the market data request                                                                    |
| 83    | RptSeq                  | Long    | Y        | Public sequence number for the final update in the snapshot by symbol                                            |
| 893   | LastFragment            | Char    | Y        | Is this the last message in the snapshot for a given symbol<br />Y=Yes<br />N=No                                 |
| 55    | Symbol                  | String  | Y        | Repeating group of symbols for which the client requests market data                                             |
| 268   | NoMDEntries             | Int     | Y        | Number of orders to be added to the book in this snapshot message                                                |
| 1682  | MDSecurityTradingStatus | String  | Y        | `trading_disabled`<br />`cancel_only`<br />`post_only`<br />`limit_only`<br />`full_trading`<br />`auction_mode` |
| =>269 | MDEntryType             | Char    | Y        | 0=Bid<br />1=Offer                                                                                               |
| =>278 | MDEntryID               | String  | Y        | The order ID that should be added to the book                                                                    |
| =>270 | MDEntryPx               | Decimal | Y        | The price of the order                                                                                           |
| =>271 | MDEntrySize             | Decimal | Y        | The quantity remaining of the order                                                                              |

## Security List Request (35=x)

This message is sent by clients to request a full list of instruments that Coinbase Exchange supports together with each instrument’s trading status, tick size, minimum order quantity, and any other descriptive fields.

| Tag | FieldName               | Type   | Required | Notes                             |
| :-- | :---------------------- | :----- | :------- | :-------------------------------- |
| 320 | SecurityReqID           | String | Y        | Client identifier for the request |
| 559 | SecurityListRequestType | Int    | Y        | Always 4=All Securities           |

## Security List (35=y)

Instrument definition messages are returned in response to a client’s Security List Request.

| Tag     | FieldName               | Type    | Required | Notes                                                                                                            |
| :------ | :---------------------- | :------ | :------- | :--------------------------------------------------------------------------------------------------------------- |
| 320     | SecurityReqID           | String  | Y        | Client identifier for the request                                                                                |
| 322     | SecurityResponseID      | String  | Y        | Response ID for the Security List Request                                                                        |
| 560     | SecurityRequestResult   | Int     | Y        | 0=Valid Request<br />1=Invalid Request                                                                           |
| 893     | LastFragment            | Char    | Y        | Is this the last instrument definition message in response to the original request<br />Y=Yes<br />N=No          |
| 393     | TotNoRelatedSym         | Int     | Y        | Total number of symbols that will be sent cumulatively                                                           |
| 146     | NoRelatedSym            | Int     | Y        | How many symbols are in this FIX message                                                                         |
| 1682    | MDSecurityTradingStatus | String  | Y        | `trading_disabled`<br />`cancel_only`<br />`post_only`<br />`limit_only`<br />`full_trading`<br />`auction_mode` |
| =>55    | Symbol                  | String  | Y        | Repeating group of symbols for which the client requests market data                                             |
| =>15    | Currency                | String  | Y        | The quote currency for the symbol (e.g., USD if 55=BTC-USD)                                                      |
| =>562   | MinTradeVol             | Decimal | Y        | The minimum notional amount in quote currency terms for an order                                                 |
| =>969   | MinPriceIncrement       | Decimal | Y        | Minimum increment for quote currency (e.g., 0.01 USD for BTC-USD)                                                |
| =>29003 | MinSizeIncrement        | Decimal | Y        | Minimum increment for base currency (e.g., 0.00000001 BTC for BTC-USD)                                           |

