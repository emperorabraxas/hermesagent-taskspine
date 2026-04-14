# open WebSocket connection and subscribe to channels
ws_client.open()
ws_client.subscribe(["BTC-USD"], ["heartbeats", "user"])
