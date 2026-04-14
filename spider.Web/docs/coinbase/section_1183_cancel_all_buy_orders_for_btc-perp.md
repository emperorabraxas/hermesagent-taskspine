# Cancel all BUY orders for BTC-PERP
request = CancelOrdersRequest(
    portfolio="PORTFOLIO_ID_HERE",
    instrument="BTC-PERP",
    side=OrderSide.BUY.value
)

response = client.orders.cancel_orders(request)
print(response)
```

