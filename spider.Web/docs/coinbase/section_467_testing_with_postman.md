# Testing with Postman
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/sandbox/postman

Use Postman to test Payment APIs via UI

## Overview

[Postman](https://www.postman.com/) is a popular API testing tool that lets you send requests and inspect responses without writing code. We provide a pre-configured collection with all Payment API endpoints ready to use.

## Prerequisites

* Postman account ([sign up](https://www.postman.com/) or use the web version)
* Sandbox API credentials from the [CDP Portal Sandbox](https://portal.cdp.coinbase.com/v2/sandbox) (covered in the [Quickstart](/api-reference/payment-apis/sandbox/quickstart))

## 1. Download files

Download both files below:

* <a href="/api-reference/payment-apis/CDP Payments Sandbox.postman_collection-docs.json">CDP Payments Collection</a>: Pre-built requests for all Payment API endpoints with the correct HTTP methods, headers, and request body templates
* <a href="/api-reference/payment-apis/CDP Payments Sandbox.postman_environment-docs.json">CDP Payments Environment</a>: Variables for the Sandbox base URL and your API keys

## 2. Import into Postman

<Steps>
  <Step title="Import collection">
    In Postman, go to **Collections** (left pane) → **Import** → upload the Collection file
  </Step>

  <Step title="Import environment">
    Go to **Environments** (left pane) → **Import** → upload the Environment file
  </Step>
</Steps>

## 3. Configure API keys

<Steps>
  <Step title="Select environment">
    In the top-right dropdown, select **CDP Payments Sandbox**
  </Step>

  <Step title="Update API key variables">
    On your variable settings, update values for `privateKey` and `name` according to your CDP Sandbox API Key you created during the [Quickstart](/api-reference/payment-apis/sandbox/quickstart)
  </Step>
</Steps>

## 4. Test requests

<Steps>
  <Step title="Open a request">
    Select any request from the collection (e.g., "List Payment Methods")
  </Step>

  <Step title="Update request body">
    For POST requests, update the request body with your test data:

    * Get account IDs from "List Accounts" request (see [Accounts guide](/api-reference/payment-apis/sandbox/guides/accounts))
    * Get payment method IDs from "List Payment Methods" request (see [Payment Methods guide](/api-reference/payment-apis/sandbox/guides/payment-methods))
    * Use test email addresses: `testuser1@domain.com` or `testuser2@domain.com` (see [Transfers guide](/api-reference/payment-apis/sandbox/guides/transfers))
  </Step>

  <Step title="Send">
    Click **Send** to execute the request
  </Step>
</Steps>

The collection handles JWT authentication automatically using your configured API keys.

<Tip>
  Start with GET requests (List Accounts, List Payment Methods) to retrieve IDs, then use those IDs in POST requests (Create Transfer, Create Deposit Destination).
</Tip>

## Available endpoints

The Postman collection includes all Sandbox endpoints:

* **[Accounts](/api-reference/payment-apis/sandbox/guides/accounts)** - Create and list accounts
* **[Deposit Destinations](/api-reference/payment-apis/sandbox/guides/deposit-destinations)** - Create and list deposit destinations
* **[Payment Methods](/api-reference/payment-apis/sandbox/guides/payment-methods)** - List payment methods and test withdrawals
* **[Transfers](/api-reference/payment-apis/sandbox/guides/transfers)** - Create, execute, and list transfers (onchain, email, payment method)

## What to read next

<CardGroup>
  <Card title="Quickstart" icon="rocket" href="/api-reference/payment-apis/sandbox/quickstart">
    Alternative setup with cdpcurl (CLI tool)
  </Card>

  <Card title="Payment APIs Overview" icon="book" href="/api-reference/payment-apis/overview">
    Learn more about Payment APIs
  </Card>
</CardGroup>

