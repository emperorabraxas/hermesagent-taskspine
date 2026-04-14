# Set up WebSocket connection
ws = websocket.WebSocketApp("wss://advanced-trade-ws.coinbase.com", on_open=on_open)
ws.run_forever()
```

### Subscribing to a Private Channel (e.g., User Channel)

Private channels require a JWT for authentication. Use the following code to subscribe to the `user` channel:

```python lines wrap theme={null}
import websocket
import json

def on_open(ws):
    jwt_token = generate_jwt()  # Replace with your JWT generation logic

    # Subscribe to the user channel
    subscribe_message = {
        "type": "subscribe",
        "channel": "user",
        "product_ids": ["BTC-USD"],
        "jwt": jwt_token
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to user channel for BTC-USD")
