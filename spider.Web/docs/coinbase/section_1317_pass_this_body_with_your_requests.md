# pass this body with your requests
message = Base64.strict_encode64(hash)
```

```python lines wrap theme={null}
def sign(channel, key, secret, account_id, product_ids):
    message = channel + key + account_id + timestamp + "".join(product_ids)
    signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode()
    return signature_b64
```

## Sequence Numbers

Most feed messages contain a sequence number. Sequence numbers are increasing integer values for each product, with each new message being exactly one sequence number greater than the one before it.

Sequence numbers that are *greater than one integer value* from the previous number indicate that a message has been dropped. Sequence numbers that are *less* than the previous number can be ignored or represent a message that has arrived out of order.

In either situation you may need to perform logic to make sure your system is in the correct state.

<Warning>
  Even though a WebSocket connection is over TCP, the WebSocket servers receive market data in a manner that can result in dropped messages. Your feed consumer should be designed to handle sequence gaps and out of order messages, or should use channels that guarantee delivery of messages.
</Warning>

<Tip>
  To guarantee that messages are delivered and your order book is in sync, consider using the [level2 channel](/prime/websocket-feed/channels).
</Tip>

