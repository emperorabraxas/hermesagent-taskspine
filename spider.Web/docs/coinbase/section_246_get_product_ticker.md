# Get product ticker
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-ticker

GET /products/{product_id}/ticker
Gets snapshot information about the last trade (tick), best bid/ask and 24h volume.

## Real-time updates

Coinbase recommends that you get real-time updates by connecting with the WebSocket stream and listening for match messages, rather than polling.

