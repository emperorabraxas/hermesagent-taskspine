# Market Data WebSocket URL
WS_URL = "wss://advanced-trade-ws.coinbase.com"

def on_open(ws):
    # Subscribe to the ticker channel for BTC-USD
    subscribe_message = {
        "type": "subscribe",
        "product_ids": ["BTC-USD"],
        "channel": "ticker"
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to BTC-USD ticker channel")

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received message: {data}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("Connection closed")
