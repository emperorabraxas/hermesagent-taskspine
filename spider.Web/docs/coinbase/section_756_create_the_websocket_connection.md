# Create the WebSocket connection
ws = websocket.WebSocketApp(
    WS_USER_URL,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()
```

In this authenticated example, we generate a JWT using the PyJWT library and include it in the subscription message for the user channel. This allows the client to receive real-time updates related to the user's orders for the BTC-USD product.

## 3. Authentication and Subscriptions

WebSocket connections that interact with user-specific data on the Coinbase Developer Platform's Advanced Trade product require authentication via JSON Web Tokens (JWTs). This section will guide developers through generating JWTs, subscribing to channels, and managing multiple subscriptions effectively.

### Generating and Using JWT Tokens

To subscribe to user-specific channels, such as the `user` or `futures_balance_summary` channels, you must include a valid JWT in the subscription message. The JWT is generated using your API key and signing key.

### Steps to Generate a JWT Token:

* Obtain your API key and signing key from the Coinbase Developer Platform.
* Use the JWT to authenticate when subscribing to user-related data channels.
* JWT tokens expire after 2 minutes, so they must be refreshed regularly.

### Example: Generating a JWT in Python

First, ensure you have the required dependencies installed:

`pip install websocket-client PyJWT cryptography`

Then, generate the JWT for authentication:

```python [expandable] lines wrap theme={null}
import jwt  # PyJWT library
import time
import uuid
