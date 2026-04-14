# Prime FIX 5.0 Messages
Source: https://docs.cdp.coinbase.com/prime/fix-5-0-api/overview

The FIX 5.0 specification can be used for and derivatives on Coinbase Prime.

<Warning>
  This specification is currently in **beta** and requires account enablement. Features and definitions are subject to change.
</Warning>

<Info>In the tables below, the **Req** column indicates whether a field is required: `Y` = Required, `N` = Optional, `C` = Conditional on another field. `↳` denotes a field within a repeating group.</Info>

<div>
  ## Session Management Messages

  ### (A) Logon

  Initiates FIX session connection between client and server.

  <br />

  <br />

  **Standard Header Fields**

  | Tag | Name         | FIX Type     | Req | Description                  |
  | :-- | :----------- | :----------- | :-- | :--------------------------- |
  | 8   | BeginString  | String       | Y   | `FIX.5.0`                    |
  | 9   | BodyLength   | Int          | Y   | Message body length in bytes |
  | 35  | MsgType      | String       | Y   | `A` = Logon                  |
  | 49  | SenderCompID | String       | Y   | Sender's unique identifier   |
  | 56  | TargetCompID | String       | Y   | Target's unique identifier   |
  | 34  | MsgSeqNum    | Int          | Y   | Message sequence number      |
  | 52  | SendingTime  | UTCTimestamp | Y   | Time of message transmission |

  **Logon Message Fields**

  | Tag  | Name             | FIX Type | Req | Description                                     |
  | :--- | :--------------- | :------- | :-- | :---------------------------------------------- |
  | 96   | RawData          | text     | Y   | Signature                                       |
  | 98   | EncryptMethod    | Int      | Y   | `0` = None                                      |
  | 108  | HeartBtInt       | Int      | Y   | Heartbeat interval in seconds (recommended: 30) |
  | 141  | ResetSeqNumFlag  | Boolean  | N   | `Y` = Reset sequence numbers to 1               |
  | 553  | Username         | String   | Y   | Client username for authentication              |
  | 554  | Password         | String   | Y   | Client password for authentication              |
  | 1137 | DefaultApplVerID | String   | Y   | `9` = FIX50SP2 = FIX 5.0 Service Pack 2         |

  ### (5) Logout

  Terminates FIX session gracefully.

  | Tag | Name | FIX Type | Req | Description                            |
  | :-- | :--- | :------- | :-- | :------------------------------------- |
  | 58  | Text | String   | N   | Logout reason or informational message |

  ### (0) Heartbeat

  Maintains session connectivity and confirms system responsiveness.

  | Tag | Name      | FIX Type | Req | Description                                                                             |
  | :-- | :-------- | :------- | :-- | :-------------------------------------------------------------------------------------- |
  | 112 | TestReqID | String   | C   | Required if responding to TestRequest. Echo the TestReqID from the TestRequest message. |

  ### (1) TestRequest

  Validates session responsiveness when no messages received within HeartBtInt period.

  | Tag | Name      | FIX Type | Req | Description                                                 |
  | :-- | :-------- | :------- | :-- | :---------------------------------------------------------- |
  | 112 | TestReqID | String   | Y   | Unique identifier that must be echoed in Heartbeat response |

  ### (3) Reject

  Indicates session-level rejection of a received message.

  | Tag | Name                | FIX Type | Req | Description                                                                                                                                     |
  | :-- | :------------------ | :------- | :-- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
  | 45  | RefSeqNum           | Int      | Y   | MsgSeqNum of rejected message                                                                                                                   |
  | 371 | RefTagID            | Int      | C   | Tag number of the field with error                                                                                                              |
  | 372 | RefMsgType          | String   | C   | MsgType of rejected message                                                                                                                     |
  | 373 | SessionRejectReason | Int      | C   | `0` = Invalid tag number<br />`1` = Required tag missing<br />`2` = Tag not defined<br />`5` = Value incorrect<br />`6` = Incorrect data format |
  | 58  | Text                | String   | N   | Human-readable description of rejection                                                                                                         |

  ### (2) ResendRequest

  Requests retransmission of messages when gap detected in sequence numbers.

  | Tag | Name       | FIX Type | Req | Description                                                         |
  | :-- | :--------- | :------- | :-- | :------------------------------------------------------------------ |
  | 7   | BeginSeqNo | Int      | Y   | Starting sequence number for resend range                           |
  | 16  | EndSeqNo   | Int      | Y   | Ending sequence number (`0` = resend all messages after BeginSeqNo) |

  ### (4) SequenceReset

  Resets message sequence numbers or fills sequence gaps.

  | Tag | Name        | FIX Type | Req | Description                                                            |
  | :-- | :---------- | :------- | :-- | :--------------------------------------------------------------------- |
  | 123 | GapFillFlag | Boolean  | C   | `Y` = Gap fill mode (messages 34 through NewSeqNo-1 have been skipped) |
  | 36  | NewSeqNo    | Int      | Y   | New sequence number for next message                                   |

  ***

  ## Order Entry Messages

  <Info>All messages in this section must include the Standard Header fields. See [(A) Logon](#a-logon) for the full field list.</Info>

  ### (D) NewOrderSingle

  Request to submit new single-legged order.

  | Tag  | Name                  | FIX Type     | Req | Description                                                                                                                                                                                                                                 |
  | :--- | :-------------------- | :----------- | :-- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | 1    | Account               | String(16)   | Y   | Trading account identifier                                                                                                                                                                                                                  |
  | 11   | ClOrdID               | String(36)   | Y   | Unique client order identifier. Must be unique across all orders.                                                                                                                                                                           |
  | 38   | OrderQty              | Int(9)       | Y   | Order quantity (positive integer)                                                                                                                                                                                                           |
  | 152  | CashOrderQty          | Int(9)       | Y   | Order quantity (in quote units)                                                                                                                                                                                                             |
  | 40   | OrdType               | Char(1)      | Y   | `1` = Market<br />`2` = Limit<br />`4` = Stop Limit                                                                                                                                                                                         |
  | 44   | Price                 | Price(20)    | C   | Limit price. Required for Limit and Stop Limit orders.                                                                                                                                                                                      |
  | 54   | Side                  | Char(1)      | Y   | `1` = Buy, `2` = Sell                                                                                                                                                                                                                       |
  | 55   | Symbol                | String(24)   | Y   | Instrument symbol (e.g., BTC-27FEB26-CDE, ETH-USD).                                                                                                                                                                                         |
  | 167  | SecurityType          | String(6)    | Y   | `FUT` = Futures                                                                                                                                                                                                                             |
  | 59   | TimeInForce           | Char(1)      | N   | `1` = Good Till Cancel (GTC)<br />`6` = Good Till Date (GTD)<br />`3` = Immediate or Cancel (IOC)<br />`4` = Fill or Kill (FOK)                                                                                                             |
  | 60   | TransactTime          | UTCTimestamp | Y   | Order submission time (YYYYMMDD-HH:MM:SS.sss in UTC)                                                                                                                                                                                        |
  | 18   | ExecInst              | Char         | N   | `A` = Post only                                                                                                                                                                                                                             |
  | 99   | StopPx                | Price(20)    | C   | Stop trigger price. Required for Stop and Stop Limit orders.                                                                                                                                                                                |
  | 126  | ExpireTime            | UTCTimestamp | C   | Expiration time. Required when TimeInForce = `6` (GTD).                                                                                                                                                                                     |
  | 168  | EffectiveTime         | UTCTimestamp | C   | Start time of an order (required for TWAP/VWAP orders)                                                                                                                                                                                      |
  | 1138 | DisplayQty            | Qty          | N   | Display quantity for iceberg orders. Only available when OrdType `2` = Limit or `4` = Stop Limit.                                                                                                                                           |
  | 528  | OrderCapacity         | Char(1)      | N   | `A` = Agency, `P` = Principal                                                                                                                                                                                                               |
  | 847  | TargetStrategy        |              | N   | Requires ExpireTime and EffectiveTime for TWAP/VWAP orders. `1001` = TWAP                                                                                                                                                                   |
  | 1028 | ManualOrderIndicator  | Boolean      | Y   | `Y` = Manual order entry, `N` = Automated/algorithmic                                                                                                                                                                                       |
  | 1031 | CustOrderHandlingInst | String       | Y   | `W` = Desk<br />`Y` = Electronic (default)<br />`C` = Vendor provided platform billed by executing broker<br />`G` = Sponsored access via exchange API<br />`H` = Premium algorithmic trading provided by executing broker<br />`D` = Other |

  ### (F) OrderCancelRequest

  Request to cancel submitted single or multi-leg order.

  | Tag  | Name                 | FIX Type     | Req | Description                                                      |
  | :--- | :------------------- | :----------- | :-- | :--------------------------------------------------------------- |
  | 1    | Account              | String(16)   | Y   | Account identifier                                               |
  | 11   | ClOrdID              | String(36)   | Y   | New unique client order identifier for this cancel request       |
  | 37   | OrderID              | String(17)   | Y   | Exchange-assigned order ID to be canceled (from ExecutionReport) |
  | 41   | OrigClOrdID          | String(36)   | N   | ClOrdID of the order being canceled                              |
  | 54   | Side                 | Char(1)      | Y   | Original order side (`1` = Buy, `2` = Sell)                      |
  | 55   | Symbol               | String(24)   | Y   | Instrument symbol                                                |
  | 167  | SecurityType         | String(6)    | Y   | `FUT`                                                            |
  | 60   | TransactTime         | UTCTimestamp | Y   | Cancel request submission time                                   |
  | 1028 | ManualOrderIndicator | Boolean      | Y   | `Y` = Manual, `N` = Automated                                    |

  ### (H) OrderStatusRequest

  Queries current status of an order.

  | Tag | Name         | FIX Type   | Req | Description                        |
  | :-- | :----------- | :--------- | :-- | :--------------------------------- |
  | 1   | Account      | String(16) | N   | Account identifier                 |
  | 11  | ClOrdID      | String(36) | Y   | Client order identifier            |
  | 37  | OrderID      | String(17) | C   | Exchange order ID (if known)       |
  | 54  | Side         | Char(1)    | Y   | Order side (`1` = Buy, `2` = Sell) |
  | 55  | Symbol       | String(24) | Y   | Instrument symbol                  |
  | 167 | SecurityType | String(6)  | Y   | `FUT`                              |

  ### (8) ExecutionReport

  Reports order status changes, fills, rejections, and other execution events.

  | Tag  | Name               | FIX Type     | Req | Description                                                                                                                                                                                                                                                                                           |
  | :--- | :----------------- | :----------- | :-- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 1    | Account            | String(16)   | Y   | Account identifier                                                                                                                                                                                                                                                                                    |
  | 11   | ClOrdID            | String(36)   | Y   | Client order identifier from request message                                                                                                                                                                                                                                                          |
  | 13   | CommType           | String       | Y   | `3` = Absolute                                                                                                                                                                                                                                                                                        |
  | 12   | Commission         | Amt          | Y   | The Coinbase commission incurred for this fill in quote currency                                                                                                                                                                                                                                      |
  | 17   | ExecID             | String       | Y   | Unique execution identifier assigned by exchange. Returns `0` when sent in with OrderStatusRequest                                                                                                                                                                                                    |
  | 30   | LastMkt            | String       | Y   | Venue of execution for last fill                                                                                                                                                                                                                                                                      |
  | 37   | OrderID            | String(17)   | Y   | Exchange-assigned order identifier                                                                                                                                                                                                                                                                    |
  | 41   | OrigClOrdID        | String(36)   | C   | Original ClOrdID when responding to cancel/replace requests                                                                                                                                                                                                                                           |
  | 150  | ExecType           | Char         | Y   | `A` = Pending New<br />`0` = New<br />`4` = Canceled<br />`8` = Rejected<br />`C` = Expired<br />`F` = Trade (partial or full fill)<br />`3` = Done for Day<br />`L` = Stop Triggered                                                                                                                 |
  | 39   | OrdStatus          | Char         | Y   | `A` = Pending New<br />`0` = New<br />`I` = Order Status <br />`1` = Partially filled<br />`2` = Filled<br />`4` = Canceled<br />`8` = Rejected<br />`C` = Expired<br />`6` = Pending Cancel<br />`E` = Pending Replace                                                                               |
  | 54   | Side               | Char(1)      | Y   | `1` = Buy, `2` = Sell                                                                                                                                                                                                                                                                                 |
  | 55   | Symbol             | String(24)   | Y   | Instrument symbol                                                                                                                                                                                                                                                                                     |
  | 167  | SecurityType       | String(6)    | Y   | `FUT`                                                                                                                                                                                                                                                                                                 |
  | 38   | OrderQty           | Int(9)       | Y   | Original order quantity                                                                                                                                                                                                                                                                               |
  | 40   | OrdType            | Char(1)      | Y   | `1` = Market<br />`2` = Limit<br />`3` = Stop<br />`4` = Stop Limit                                                                                                                                                                                                                                   |
  | 44   | Price              | Price(20)    | C   | Limit price (if applicable)                                                                                                                                                                                                                                                                           |
  | 99   | StopPx             | Price(20)    | C   | Stop trigger price (if applicable)                                                                                                                                                                                                                                                                    |
  | 59   | TimeInForce        | Char(1)      | N   | `1` = GTC<br />`6` = GTD<br />`3` = IOC<br />`4` = FOK                                                                                                                                                                                                                                                |
  | 60   | TransactTime       | UTCTimestamp | Y   | Transaction time (YYYYMMDD-HH:MM:SS.ssssss)                                                                                                                                                                                                                                                           |
  | 14   | CumQty             | Qty          | Y   | Cumulative quantity filled                                                                                                                                                                                                                                                                            |
  | 151  | LeavesQty          | Qty          | Y   | Quantity remaining open (OrderQty - CumQty)                                                                                                                                                                                                                                                           |
  | 152  | CashOrderQty       | Qty          | Y   | Quantity remaining in quote currency                                                                                                                                                                                                                                                                  |
  | 32   | LastQty            | Qty          | C   | Quantity filled in this execution (required when ExecType = `F`)                                                                                                                                                                                                                                      |
  | 31   | LastPx             | Price(20)    | C   | Execution price (required when ExecType = `F`)                                                                                                                                                                                                                                                        |
  | 6    | AvgPx              | Price(20)    | Y   | Average fill price across all executions                                                                                                                                                                                                                                                              |
  | 136  | NoMiscFees         |              | C   | Number of MiscFees (repeating group)                                                                                                                                                                                                                                                                  |
  | ↳137 | MiscFeeAmt         | Amt          | C   | Misc fee value                                                                                                                                                                                                                                                                                        |
  | ↳138 | MiscFeeCurr        | String       | C   | Currency of misc fees in quote currency                                                                                                                                                                                                                                                               |
  | ↳139 | MiscFeeType        | String       | C   | `1` = Regulatory Fee<br />`7` = Client Fee<br />`4` = Venue Fee<br />`3` = Trading Desk Fee<br />`14` = Financing Fee<br />`31` = Clearing Fee                                                                                                                                                        |
  | 103  | OrdRejReason       | Int          | C   | Required when ExecType = `8` (Rejected):<br />`1` = Unknown symbol<br />`2` = Exchange closed<br />`3` = Order exceeds limit<br />`4` = Too late to enter<br />`5` = Unknown order<br />`6` = Duplicate order<br />`8` = Stale order<br />`18` = Invalid price increment<br />`99` = Other (see Text) |
  | 58   | Text               | String       | N   | Rejection reason or other informational message                                                                                                                                                                                                                                                       |
  | 168  | EffectiveTime      | UTCTimestamp | C   | Start time of an order (required for TWAP/VWAP)                                                                                                                                                                                                                                                       |
  | 126  | ExpireTime         | UTCTimestamp | C   | Expiration time (when TimeInForce = GTD)                                                                                                                                                                                                                                                              |
  | 1138 | DisplayQty         | Qty          | C   | Display quantity for iceberg orders. Only available when OrdType `2` = Limit or `4` = Stop Limit                                                                                                                                                                                                      |
  | 528  | OrderCapacity      | Char(1)      | N   | `A` = Agency, `P` = Principal                                                                                                                                                                                                                                                                         |
  | 1057 | AggressorIndicator | Boolean      | N   | `Y` = Aggressor, `N` = Passive (for trade reporting)                                                                                                                                                                                                                                                  |

  ***

  ## Appendix A: Code Sets

  ### OrdType (40)

  | Value | Description |
  | :---- | :---------- |
  | 1     | Market      |
  | 2     | Limit       |
  | 3     | Stop        |
  | 4     | Stop Limit  |

  ### Side (54)

  | Value | Description |
  | :---- | :---------- |
  | 1     | Buy         |
  | 2     | Sell        |

  ### SecurityType (167)

  | Value | Description |
  | :---- | :---------- |
  | FUT   | Futures     |

  ### TimeInForce (59)

  | Value | Description               |
  | :---- | :------------------------ |
  | 1     | Good Till Cancel (GTC)    |
  | 3     | Immediate or Cancel (IOC) |
  | 4     | Fill or Kill (FOK)        |
  | 6     | Good Till Date (GTD)      |

  ### ExecType (150)

  | Value | Description                  |
  | :---- | :--------------------------- |
  | 0     | New                          |
  | 3     | Done for Day                 |
  | 4     | Canceled                     |
  | 5     | Replace                      |
  | 8     | Rejected                     |
  | A     | Pending New                  |
  | C     | Expired                      |
  | F     | Trade (partial or full fill) |
  | I     | Order Status                 |
  | L     | Stop Triggered               |

  ### OrdStatus (39)

  | Value | Description      |
  | :---- | :--------------- |
  | 0     | New              |
  | 1     | Partially filled |
  | 2     | Filled           |
  | 4     | Canceled         |
  | 6     | Pending Cancel   |
  | 8     | Rejected         |
  | A     | Pending New      |
  | C     | Expired          |
  | E     | Pending Replace  |
</div>

