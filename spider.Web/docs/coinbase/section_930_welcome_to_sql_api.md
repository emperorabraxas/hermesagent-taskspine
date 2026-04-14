# Welcome to SQL API
Source: https://docs.cdp.coinbase.com/data/sql-api/welcome



The SQL API is a zero-infrastructure indexing solution that allows any developer to pull real-time and historical onchain data on Base using custom SQL queries. Unlike Address History API which provides fixed endpoints for wallet data, SQL API gives you complete flexibility to query any blockchain data.

<Card title="Try it now: Quickstart" icon="rocket" href="/data/sql-api/quickstart">
  Run your first query in the SQL Playground—no API keys required
</Card>

Developers can access the SQL API through:

<CardGroup>
  <Card title="SQL Playground" icon="browser" href="https://portal.cdp.coinbase.com/products/data/playground">
    Try queries in your browser (no API keys needed)
  </Card>

  <Card title="REST API" icon="code" href="/data/sql-api/rest-apis">
    Programmatic access with free API keys
  </Card>
</CardGroup>

## Key Features

* **Zero Infra:** No setup, no guesswork. Just real-time indexed onchain data.
* **Customizable:** Leverage familiar SQL syntax to pull custom data.
* **Responsive:** Pull custom onchain data with \< 500ms latency.
* **Fresh:** \< 250ms end-to-end from tip of chain.

## Use Cases

* **Payment Service Providers:** Track real-time stablecoin transactions for merchants, consumers, and marketplaces.
* **Portfolio & Treasury:** Give users and institutions a live view of wallet balances and historical flows. Build dashboards that update instantly as funds move across chains, protocols, and counterparties.
* **Onchain Games:** Track player inventory, asset upgrades, and progression in real time as NFT metadata evolves. Enable game mechanics that reflect actual onchain state — not stale snapshots.
* **Onchain Social:** Monitor user interactions like tips, follows, and reactions across decentralized social graphs. Surface meaningful engagement and value transfer between users, apps, and agents.

## Schema

The SQL API runs queries against an opinionated schema for efficient organization and response delivery. You can read more in the [schema reference](/data/sql-api/schema). For the CoinbaSeQL grammar, you can find that in the [CoinbaSeQL reference](/data/sql-api/sql).

## Pricing & Rate Limits

SQL API operates on a pay-as-you-go model:

* **1,000 free queries every month**
* **After the free tier:** \$0.0083 per query
* **Rate limit:** 5 queries every second per project

## Support and feedback

Join **#onchain-data** in the [CDP Discord](https://discord.com/invite/cdp) to access FAQs, schedule project discussions, and connect with other developers. We welcome your feedback and suggestions for improvement.

