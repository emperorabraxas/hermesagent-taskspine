# wait for order to fill
while not order_filled:
    ws_client.sleep_with_exception_check(1)

print(f"order {limit_order_id} filled!")
ws_client.close()
```

And we are done!

You can now use the WebSocket SDK to subscribe to channels and receive real-time updates from the Coinbase Advanced API.

