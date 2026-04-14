# Exchange WebSocket Authentication
Source: https://docs.cdp.coinbase.com/exchange/websocket-feed/authentication



The following WebSocket feeds require authentication:

* [Full channel](/exchange/websocket-feed/channels#full-channel)
* [User channel](/exchange/websocket-feed/channels#user-channel)
* [Level2 channel](/exchange/websocket-feed/channels#level2-channel)
* [Level3 channel](/exchange/websocket-feed/channels#level3-channel)
* [RFQ Matches Channel](/exchange/websocket-feed/channels/#rfq-matches-channel)

To authenticate, send a `subscribe` message and pass in fields to `GET /users/self/verify`, just as if you were [signing a request](/exchange/rest-api/authentication#signing-a-message). To get the necessary parameters, go through the same process as you would to make [authenticated calls to the API](/exchange/rest-api/authentication#signing-requests).

<Warning>
  Authenticated feed messages do not increment the [sequence number](/exchange/websocket-feed/overview#sequence-numbers), which means that it is currently not possible to detect if an authenticated feed message was dropped.
</Warning>

## Examples

A Python example of authenticating a WebSocket connection is shown below. This code sample can be cloned at [Coinbase Samples](https://github.com/coinbase-samples/exchange-scripts-py/tree/main/websocket).

```python [expandable] lines wrap theme={null}
API_KEY = str(os.environ.get('API_KEY'))
PASSPHRASE = str(os.environ.get('PASSPHRASE'))
SECRET_KEY = str(os.environ.get('SECRET_KEY'))

URI = 'wss://ws-feed.exchange.coinbase.com'
SIGNATURE_PATH = '/users/self/verify'

channel = 'level2'
product_ids = 'ETH-USD'

async def generate_signature():
    timestamp = str(time.time())
    message = f'{timestamp}GET{SIGNATURE_PATH}'
    hmac_key = base64.b64decode(SECRET_KEY)
    signature = hmac.new(
        hmac_key,
        message.encode('utf-8'),
        digestmod=hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode().rstrip('\n')
    return signature_b64, timestamp


async def websocket_listener():
    signature_b64, timestamp = await generate_signature()
    subscribe_message = json.dumps({
        'type': 'subscribe',
        'channels': [{'name': channel, 'product_ids': [product_ids]}],
        'signature': signature_b64,
        'key': API_KEY,
        'passphrase': PASSPHRASE,
        'timestamp': timestamp
    })
```

Further examples are shown below:

```json lines wrap theme={null}
// Authenticated feed messages add user_id and
// profile_id for messages related to your user
{
  "type": "open", // "received" | "open" | "done" | "match" | "change" | "activate"
  "user_id": "5844eceecf7e803e259d0365",
  "profile_id": "765d1549-9660-4be2-97d4-fa2d65fa3352"
  /* ... */
}
```

Here's an example of an authenticated `subscribe` request:

```json lines wrap theme={null}
// Request
{
  "type": "subscribe",
  "product_ids": ["BTC-USD"],
  "channels": ["full"],
  "signature": "...",
  "key": "...",
  "passphrase": "...",
  "timestamp": "..."
}
```

## Benefits

Coinbase recommends that you authenticate *all* WebSocket channels, but only those listed above are enforced. You can authenticate yourself when [subscribing](/exchange/websocket-feed/overview#subscribe) to the WebSocket Feed. The benefits of authenticating are:

* Messages (in which you are of the parties) are expanded and have more useful fields.
* You receive private messages, such as lifecycle information about stop orders you placed.

