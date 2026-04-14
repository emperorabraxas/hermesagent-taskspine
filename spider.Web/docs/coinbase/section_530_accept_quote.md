# Accept Quote
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/accept-quote

POST /v1/portfolios/{portfolio_id}/accept_quote
Accepts the quote received by the quote request and creates an order with the provided quote ID.

Always required: portfolio_id, product_id, side, quote_id, client_quote_id.


