# FAQ & Resources
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/migrate/faq



## FAQ

### Do I need to update my request bodies?

No. The Checkouts API accepts the same request body schema as the Payment Link API. The only change is the URL path (`/api/v1/checkouts` instead of `/api/v1/payment-links`).

### Do my existing payment links still work?

Yes. Existing payment links continue to function. The Payment Link API will remain available during the migration period. You can migrate at your own pace.

### Can I use the same API keys?

Yes. The Checkouts API uses the same CDP API key authentication as the Payment Link API. No changes to your credentials are needed.

### How do I handle both APIs during the transition?

Run webhook subscriptions for both `payment_link.*` and `checkout.*` event types in parallel while you migrate. Once all your payment requests are created through the Checkouts API and you've confirmed webhook delivery, delete the old Payment Link subscriptions.

### What cryptocurrencies are supported?

The Checkouts API supports USDC on Base. Support for additional networks and tokens will be added in the future.

### Can I update a checkout after creation?

Checkouts cannot be updated after creation. To change details, deactivate the existing checkout and create a new one.

### How do I monitor checkout status?

Use webhooks for real-time notifications. See the [Webhooks documentation](/coinbase-business/checkout-apis/webhooks) for setup instructions. Alternatively, poll the GET endpoint to check status periodically.

## Support and resources

<CardGroup>
  <Card title="Checkouts API docs" icon="book" href="/coinbase-business/checkout-apis/overview">
    New API documentation and guides
  </Card>

  <Card title="API reference" icon="code" href="/api-reference/business-api/rest-api/checkouts/introduction">
    Complete endpoint reference
  </Card>

  <Card title="Authentication guide" icon="key" href="/api-reference/v2/authentication">
    CDP API key setup and JWT tokens
  </Card>

  <Card title="Developer Discord" icon="discord" href="/support/join-cdp-discord">
    Get help from the community
  </Card>
</CardGroup>

