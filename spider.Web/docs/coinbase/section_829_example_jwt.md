# Example JWT
token = generate_jwt()
print(f"Generated JWT: {token}")
```

This JWT must be included in all subscription messages for user-specific channels.

### Subscribing to Channels

To receive data from WebSocket channels, you need to send a subscription message after establishing the WebSocket connection. Each channel subscription must specify the product IDs (e.g., BTC-USD, ETH-USD) and, if required, a JWT for authentication.

### Example Subscription Message (Authenticated User Channel)

Here’s how to subscribe to the `user` channel for receiving updates on your orders:

```python lines wrap theme={null}
subscribe_message = {
    "type": "subscribe",
    "channel": "user",
    "product_ids": ["BTC-USD"],
    "jwt": generate_jwt()
}
```

### Example Subscription Message (Market Data Channel)

For public market data, no JWT is required:

```python lines wrap theme={null}
subscribe_message = {
    "type": "subscribe",
    "product_ids": ["BTC-USD", "ETH-USD"],
    "channel": "ticker"
}
```

### Channel Overview

Coinbase Advanced Trade WebSockets provide access to multiple channels, each serving different purposes. Below is an overview of the available channels:

| Channel                   | Description                                                   | Authentication Required |
| :------------------------ | :------------------------------------------------------------ | :---------------------- |
| ticker                    | Real-time price updates every time a match happens            | No                      |
| ticker\_batch             | Real-time price updates every 5000 milliseconds               | No                      |
| market\_trades            | Real-time updates every time a market trade happens           | No                      |
| status                    | Sends all products and currencies on a preset interval        | No                      |
| level2                    | All updates and easiest way to keep order book snapshot       | No                      |
| candles                   | Price updates aggregated into time intervals                  | No                      |
| user                      | Only sends messages that include the authenticated user       | Yes                     |
| heartbeats                | Real-time server pings to keep all connections open           | No                      |
| futures\_balance\_summary | Real-time updates every time a user's futures balance changes | Yes                     |

Each subscription can handle only one channel at a time, so if you want to receive data from multiple channels, send a separate subscription message for each.

### Best Practices for Subscriptions

1. **Load Balancing Across WebSocket Connections**
   When subscribing to multiple channels or products, it is recommended to spread the load across different WebSocket connections. For example, instead of subscribing to multiple high-volume products (like BTC-USD and ETH-USD) on the same connection, open separate WebSocket connections for each. This reduces the risk of dropped messages and helps distribute inbound traffic more efficiently.
2. **Using the Heartbeats Channel**
   The `heartbeats` channel sends periodic heartbeat messages to ensure the WebSocket connection remains active, especially when there are no frequent updates in other channels (e.g., illiquid markets). It is a best practice to subscribe to the `heartbeats` channel alongside other channels to prevent connections from closing due to inactivity.

### Example Heartbeats Subscription:

```python lines wrap theme={null}
subscribe_message = {
    "type": "subscribe",
    "channel": "heartbeats"
}
```

Including the heartbeats subscription ensures that the WebSocket connection stays open, even when there is a lack of updates on other subscribed channels.

## 4. WebSocket Channels Overview

Coinbase’s Advanced Trade WebSockets offer various channels that provide real-time market data and user-specific information. This section gives an overview of the available channels, indicates which channels require authentication, and provides sample code to subscribe and unsubscribe from these channels.

### Which Channels Require Authentication?

* Public Channels (No Authentication Required): These channels are used to receive market data and do not require authentication. They include:
  * level2
  * ticker
  * ticker\_batch
  * candles
  * heartbeats
  * market\_trades
  * status

* Private Channels (JWT Authentication Required): These channels provide user-specific data and require the inclusion of a valid JWT token in the subscription message. They include:
  * user
  * futures\_balance\_summary

### Sample Code for Subscriptions

Below are examples of how to subscribe to and unsubscribe from various channels using Python. These examples demonstrate both public and private channels.

### Subscribing to a Public Channel (e.g., Ticker Channel)

Public channels do not require authentication, so you can simply send a subscription message after establishing the WebSocket connection.

```python lines wrap theme={null}
import websocket
import json

def on_open(ws):
    # Subscribe to the ticker channel for BTC-USD
    subscribe_message = {
        "type": "subscribe",
        "product_ids": ["BTC-USD"],
        "channel": "ticker"
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to BTC-USD ticker channel")
