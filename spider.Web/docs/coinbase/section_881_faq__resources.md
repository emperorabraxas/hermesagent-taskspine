# FAQ & Resources
Source: https://docs.cdp.coinbase.com/coinbase-business/payment-link-apis/migrate/faq



## FAQ

### Can I still use the Charge API?

We recommend migrating to the Payment Link API to take advantage of improved reliability and new features.

### What cryptocurrencies are supported?

Payment Link API supports USDC across multiple chains: Ethereum, Base, Polygon, Optimism, and Arbitrum. The payer pays \$0 in gas costs across all chains. The Commerce Charge API supported multiple cryptocurrencies through automatic conversion. Payment Link focuses on stablecoins for predictable settlement.

### How do I handle multiple payment options?

Create multiple payment links for different amounts or purposes. Each payment link has a unique URL and ID.

### Can I update a payment link after creation?

Payment links cannot be updated after creation. To change details, deactivate the existing link and create a new one.

### What happens to existing Charge webhooks?

Existing Commerce webhooks will continue to work for Charge API. For Payment Link API, webhook support is available. See the [Webhooks documentation](/coinbase-business/payment-link-apis/webhooks) to set up real-time payment status notifications.

### How do I monitor payment status?

You can monitor payment status using webhooks for real-time notifications. See the [Webhooks documentation](/coinbase-business/payment-link-apis/webhooks) for setup instructions. Alternatively, you can periodically poll the GET endpoint to check the payment link status.

### Can customers pay with different cryptocurrencies?

Payment Link API supports USDC on Ethereum, Base, Polygon, Optimism, and Arbitrum. Customers can pay from any of these supported chains with \$0 gas costs.

## Support and resources

<CardGroup>
  <Card title="Payment Link API docs" icon="book" href="/coinbase-business/payment-link-apis/overview">
    New API documentation and guides
  </Card>

  <Card title="API reference" icon="code" href="/api-reference/business-api/rest-api/payment-links">
    Complete endpoint reference
  </Card>

  <Card title="Authentication guide" icon="key" href="/api-reference/v2/authentication">
    CDP API key setup and JWT tokens
  </Card>

  <Card title="Developer Discord" icon="discord" href="/support/join-cdp-discord">
    Get help from the community
  </Card>
</CardGroup>

