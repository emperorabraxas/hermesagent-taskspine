# Webhooks
Source: https://docs.cdp.coinbase.com/get-started/webhooks



Coinbase Developer Platform supports webhook subscriptions across several products, all using the same underlying API and authentication. Use webhooks to receive real-time HTTP notifications when events happen onchain, in your wallets, or across your CDP accounts.

## Getting started

Before you get started, ensure you have:

<AccordionGroup>
  <Accordion title="A Secret API Key">
    Sign up at [portal.cdp.coinbase.com](https://portal.cdp.coinbase.com), then navigate to [API Keys](https://portal.cdp.coinbase.com/projects/api-keys) and select **Create API key** under the **Secret API Keys** tab.

    1. Enter an API key nickname (restrictions are optional)
    2. Click **Create**
    3. Secure your API Key ID and Secret in a safe location
  </Accordion>

  <Accordion title="A webhook URL">
    You'll need an HTTPS URL to receive webhook events. For quick testing, [webhook.site](https://webhook.site) gives free temporary URLs instantly.

    For production, use your own HTTPS endpoint.
  </Accordion>

  <Accordion title="cdpcurl">
    Install `cdpcurl` to make authenticated requests to CDP APIs:

    ```bash theme={null}
    # With Homebrew
    brew tap coinbase/cdpcurl && brew install cdpcurl

    # Or with Go
    go install github.com/coinbase/cdpcurl@latest
    ```
  </Accordion>
</AccordionGroup>

## Subscribe by product

**Webhook support is actively expanding across CDP products.** Check back as more integrations are added.

<CardGroup>
  <Card title="Onchain Data" icon="wave-pulse" href="/data/webhooks/quickstart">
    Monitor smart contract events and token transfers on Base.
  </Card>

  <Card title="Server Wallets" icon="wallet" href="/server-wallets/v2/using-the-wallet-api/webhooks">
    Track transfer activity in and out of your CDP Server Wallet addresses.
  </Card>

  <Card title="Embedded Wallets" icon="mobile" href="/data/webhooks/quickstart">
    Track transfer activity on your users' wallets using Onchain Data Webhooks. **Native Embedded Wallet webhook support is coming soon.**
  </Card>

  <Card title="Onramp & Offramp" icon="money-bill-transfer" href="/onramp/core-features/webhooks">
    Receive real-time status updates for your users' buy and sell transactions.
  </Card>
</CardGroup>

