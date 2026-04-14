# Create the WebSocket connection
ws = websocket.WebSocketApp(
    WS_URL,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
ws.run_forever()
```

In this example, once the connection is established, the client sends a subscription message to the `ticker` channel for the BTC-USD product. The WebSocket then begins streaming real-time price updates for that product.

### Example: Connecting With Authentication (User Order Data Endpoint)

For user-specific data, such as order updates, you must authenticate using a JWT. Below is an example in Python that connects to the User Order Data WebSocket and subscribes to the `user` channel.
First, let’s install the necessary dependencies:

```python [expandable] lines wrap theme={null}
pip install websocket "pyjwt[crypto]"


import websocket
import json
import jwt  # PyJWT library
import time
import uuid
