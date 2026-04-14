# Example API and Signing Keys (replace with actual values)
API_KEY = "organizations/{org_id}/apiKeys/{key_id}"
SIGNING_KEY = "-----BEGIN EC PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END EC PRIVATE KEY-----\n"

def generate_jwt():
    current_time = int(time.time())
    payload = {
        "iss": "cdp",
        "nbf": current_time,
        "exp": current_time + 120,  # valid for 120 seconds
        "sub": API_KEY,
    }
    headers = {
        "kid": API_KEY,
        "nonce": uuid.uuid4().hex
    }
    token = jwt.encode(payload, SIGNING_KEY, algorithm="ES256", headers=headers)
    return token
