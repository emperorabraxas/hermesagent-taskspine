# CDP Payments API
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/overview



CDP Payments API helps you build end-to-end stablecoin money movement flows, from funding and transfer execution to lifecycle tracking through webhooks.

## Getting started

* **Review API basics:** See [API and network support](/api-reference/payment-apis/supported-networks-assets) and [Conventions](/api-reference/payment-apis/conventions).
* **Test before going live:** Check out the [CDP Sandbox](/api-reference/payment-apis/sandbox/overview).
* **Build a transfer flow:** Read the [Transfers overview](/api-reference/payment-apis/rest-api/transfers/transfers) to design transfer creation and execution, then subscribe to [webhooks](/api-reference/payment-apis/webhooks) for status updates.

## Local testing

<CardGroup>
  <Card title="Sandbox" icon="flask" href="/api-reference/payment-apis/sandbox/overview">
    Overview of the CDP Payments sandbox environment.
  </Card>

  <Card title="Sandbox Quickstart" icon="rocket" href="/api-reference/payment-apis/sandbox/quickstart">
    Run through a guided local testing flow.
  </Card>

  <Card title="Postman" icon="paper-plane" href="/api-reference/payment-apis/sandbox/postman">
    Test endpoints quickly with a Postman collection.
  </Card>
</CardGroup>

## Resource guides

<CardGroup>
  <Card title="Accounts" icon="wallet" href="/api-reference/payment-apis/rest-api/accounts/accounts">
    Understand account concepts and account-related flows.
  </Card>

  <Card title="Deposit Destinations" icon="inbox" href="/api-reference/payment-apis/rest-api/deposit-destinations-under-development/overview">
    Learn how deposit destinations are used in payment workflows.
  </Card>

  <Card title="Payment Methods" icon="credit-card" href="/api-reference/payment-apis/rest-api/payment-methods/payment-methods">
    Understand payment method resources used as transfer participants.
  </Card>

  <Card title="Transfers" icon="arrows-rotate" href="/api-reference/payment-apis/rest-api/transfers/transfers">
    Learn transfer lifecycle, validation, and payload shape patterns.
  </Card>

  <Card title="Webhooks" icon="webhook" href="/api-reference/payment-apis/webhooks">
    Configure webhook delivery and verify incoming events.
  </Card>
</CardGroup>

## OpenAPI Spec

<Card title="Download OpenAPI Spec" icon="download" href="https://docs.cdp.coinbase.com/api-reference/payment-apis/payment-apis-spec.yaml">
  To use with Postman or to generate client SDKs.
</Card>

