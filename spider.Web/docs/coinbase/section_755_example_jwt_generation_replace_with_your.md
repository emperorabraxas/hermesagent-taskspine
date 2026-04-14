# Example JWT generation (Replace with your actual API_KEY and SIGNING_KEY)
API_KEY = "organizations/{org_id}/apiKeys/{key_id}"
SIGNING_KEY = "-----BEGIN EC PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END EC PRIVATE KEY-----\n"

def generate_jwt():
    current_time = int(time.time())
    payload = {
        "iss": "cdp",
        "nbf": current_time,
        "exp": current_time + 120,  # JWT valid for 120 seconds
        "sub": API_KEY,
    }
    headers = {
        "kid": API_KEY,
        "nonce": uuid.uuid4().hex
    }
    return jwt.encode(payload, SIGNING_KEY, algorithm="ES256", headers=headers)

def on_open(ws):
    # Generate JWT
    token = generate_jwt()

    # Subscribe to the user channel for BTC-USD orders
    subscribe_message = {
        "type": "subscribe",
        "channel": "user",
        "product_ids": ["BTC-USD"],
        "jwt": token
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to user channel for BTC-USD orders")

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received message: {data}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("Connection closed")
