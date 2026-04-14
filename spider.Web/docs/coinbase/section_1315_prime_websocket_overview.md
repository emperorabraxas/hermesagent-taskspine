# Prime WebSocket Overview
Source: https://docs.cdp.coinbase.com/prime/websocket-feed/overview



The WebSocket feed provides real-time market data updates for orders and trades.

<Info>
  WebSocket Endpoint URL

  `wss://ws-feed.prime.coinbase.com`
</Info>

## Rate Limits

Real-time market data updates provide the fastest insight into order flow and trades. You are responsible for reading the message stream and using the message relevant for your needs—this can include building real-time order books or tracking real-time trades.

### Specs

The WebSocket feed is publicly available. Connection requests to it are rate-limited at **750 every 10 seconds per IP**.

<Info> Note: All Prime infrastructure is located in AWS US-east 1 region. For optimal performance and latency, its recommended that client deploy their applications in AWS US-EAST 1. </Info>

### Errors

An error message displays when the client is actively disconnected for any of these reasons:

* The client has too many backed up messages (`ErrSlowConsume`).
* The client is sending too many messages (`ErrSlowRead`).
* The message size is too large (`Message too big`)
* There are intermittent network issues.

## Protocol

The WebSocket feed uses a bidirectional protocol that encodes all messages as JSON objects. All messages have a `type` attribute that can be used to handle the message appropriately.

<Tip>
  New message types can be added at any time. Clients are expected to ignore messages they do not support.
</Tip>

**Error messages:**
Most failure cases trigger an `error` message—specifically, a message with the `type` `"error"`. This can be helpful when implementing a client or debugging issues.

```json lines wrap theme={null}
{
  "type": "error",
  "message": "error message"
  /* ... */
}
```

## Subscribing

To begin receiving feed messages, you must send a **signed** `subscribe` message to the server indicating which channels and products to receive. This message is mandatory—you are disconnected if no `subscribe` has been received within 5 seconds.

<Warning>
  Every `subscribe` request must be signed. See [Signing Messages](#signing-messages) below.
</Warning>

```json lines wrap theme={null}
// Request -> Subscribe to heartbeat channel
{
  "type": "subscribe",
  "channel": "heartbeat",
  "access_key": "ACCESS_KEY",
  "api_key_id": "SVC_ACCOUNTID",
  "timestamp": "TIMESTAMP",
  "passphrase": "PASSPHRASE",
  "signature": "signature",
  "portfolio_id": "PORTFOLIO_ID",
  "product_ids": ["BTC-USD"]
}
```

```json lines wrap theme={null}
// Response -> heartbeat channel
{
  "channel": "subscriptions",
  "timestamp": "2022-01-25T20:52:59.353824785Z",
  "sequence_num": 0,
  "events": [
    {
      "subscriptions": {
        "heartbeat": ["heartbeat"]
      }
    }
  ]
}
```

```json lines wrap theme={null}
// Message 1:
{
  "channel": "heartbeat",
  "timestamp": "2022-01-25T20:53:01.66270911Z",
  "sequence_num": 1,
  "events": [
    {
      "current_time": "2022-01-25 20:53:01.662698745 +0000 UTC m=+3551940.494451923",
      "heartbeat_counter": 118398
    }
  ]
}
```

Once a `subscribe` message is received the server responds with a `subscriptions` message that lists all channels you are subscribed to. Subsequent subscribe messages add to the list of subscriptions.

## Unsubscribing

To unsubscribe from channel/product pairs, send an `unsubscribe` message. The structure is equivalent to `subscribe` messages.

```json lines wrap theme={null}
// Request -> unsubscribe from heartbeat channel
{
  "type": "unsubscribe",
  "channel": "heartbeat",
  "access_key": "ACCESS_KEY",
  "api_key_id": "SVC_ACCOUNTID",
  "timestamp": "TIMESTAMP",
  "passphrase": "PASSPHRASE",
  "signature": "signature",
  "portfolio_id": "",
  "product_ids": ["BTC-USD"]
}
```

<Tip>
  You can also unsubscribe from a channel entirely by providing no product IDs.
</Tip>

```json lines wrap theme={null}
// Request
{
  "type": "unsubscribe",
  "channels": ["heartbeat"]
}
```

As a response to an `unsubscribe` message you will receive a `subscriptions` message:

```json lines wrap theme={null}
{
  "channel": "subscriptions",
  "timestamp": "2022-02-19T19:59:56.701617197Z",
  "sequence_num": 0,
  "events": [
    {
      "subscriptions": {}
    }
  ]
}
```

## Signing Messages

You must authenticate yourself when subscribing to any of the Prime WebSocket channels.

Construct a payload schema for all channels with the following list of properties and valid values:

* `type`: "subscribe" or "unsubscribe"
* `channel`: WebSocket channel to subscribe to
* `access_key`: Public API key
* `api_key_id`: Service account ID
* `timestamp`: [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) for requests (seconds since the epoch); or [Epoch](https://en.wikipedia.org/wiki/Epoch_\(computing\)) for [creating signatures](/prime/rest-api/authentication#creating-a-signature). Valid ISO 8601 format: `%Y-%M-%DT%H:%M:%SZ`, for example, `2022-02-19T20:05:22Z`.
* `passphrase`: Your API passphrase
* `signature`: SHA256 HMAC signature using the prehash string and API secret key
* `portfolio_id` / `order_id`: The portfolio or order ID (depending on which feed you're subscribing to. `portfolio_id` is required for `orders` channel.)
* `product_ids`: Comma-separated list of products to subscribe to (`["BTC-USD"]`)

The `signature` field is generated by creating a SHA256 HMAC by signing your API Secret key with a prehash string. The final prehash payload is generated by creating a concatenated string of `channelName + accessKey + svcAccountId + timestamp + portfolioId + products` (where `+` represents string concatenation).

Apply a SHA256 HMAC using your secret key on this prehash payload, and then base64-encode it as your final payload within your request. Pass the output of this SHA256 HMAC to the `signature` field in each request message. See the examples of generating this `signature` below.

<Info>
  For requests that subscribe to multiple products (e.g., `product_ids: ["BTC-USD", "ETH-USD"]`), the `product_ids` string in the prehash must be formatted as follows: `BTC-USDETH-USD`.
</Info>

```ruby lines wrap theme={null}
timestamp = Time.now.to_i
string = "#{channelName}#{accessKey}#{svcAcctId}#{timestamp}#{portfolioId}";