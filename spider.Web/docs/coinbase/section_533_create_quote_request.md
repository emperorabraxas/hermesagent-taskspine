# Create Quote Request
Source: https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/orders/create-quote-request

POST /v1/portfolios/{portfolio_id}/rfq
A Quote Request is the start of the RFQ process. Coinbase Prime sends a Quote Request to Liquidity Providers (LPs) on behalf of a customer looking to participate in an RFQ trade.

Always required: portfolio_id, product_id, side, client_quote_id, and limit_price. One of either base_quantity or quote_value is always required.


