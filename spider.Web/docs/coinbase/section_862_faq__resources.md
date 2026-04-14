# FAQ & Resources
Source: https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/migrate-from-commerce/faq



## FAQ

### Can I still use the Charge API?

We recommend migrating to the Checkouts API to take advantage of improved reliability, new features like settlement details, and modernized authentication.

### What cryptocurrencies are supported?

The Checkouts API supports USDC on Base. Support for additional networks and tokens will be added in the future.

### How do I handle multiple payment options?

Create multiple checkouts for different amounts or purposes. Each checkout has a unique URL and ID.

### Can I update a checkout after creation?

Checkouts cannot be updated after creation. To change details, deactivate the existing checkout and create a new one.

### What happens to existing Charge webhooks?

Existing Commerce webhooks will continue to work for the Charge API. For the Checkouts API, set up new webhook subscriptions with `checkout.*` event types. See the [Webhooks documentation](/coinbase-business/checkout-apis/webhooks) for setup instructions.

### How do I monitor payment status?

Use webhooks for real-time notifications. See the [Webhooks documentation](/coinbase-business/checkout-apis/webhooks) for setup instructions. Alternatively, poll the GET endpoint to check checkout status periodically.

### Can customers pay with different cryptocurrencies?

The Checkouts API currently supports USDC on Base. Support for additional networks will be added in the future.

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

