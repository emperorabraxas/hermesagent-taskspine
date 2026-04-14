# get current price of BTC-USD and place limit-buy order 5% below
product = rest_client.get_product("BTC-USD")
btc_usd_price = float(product["price"])
adjusted_btc_usd_price = str(math.floor(btc_usd_price - (btc_usd_price * 0.05)))

limit_order = rest_client.limit_order_gtc_buy(
    client_order_id="00000003",
    product_id="BTC-USD",
    base_size="0.0002",
    limit_price=adjusted_btc_usd_price
)

limit_order_id = limit_order["order_id"]
