# CDP CLI
Source: https://docs.cdp.coinbase.com/get-started/tools/cdp-cli

Authenticate once, access every CDP API from the terminal or an AI agent.

`@coinbase/cdp-cli` is a CLI and [MCP](https://modelcontextprotocol.io) server for the [CDP API](/api-reference/v2/introduction). It handles authentication, provides inline documentation for every endpoint, and exposes the full API surface as typed tools for AI agents.

## Why CDP CLI

<CardGroup>
  <Card title="Auth-transparent" icon="key">
    Configure credentials once per environment. The CLI handles JWT signing for every request.
  </Card>

  <Card title="AI-native" icon="microchip-ai">
    Doubles as an MCP server with bundled agent skills. New API features become available the moment the CLI updates.
  </Card>

  <Card title="Inline schema discovery" icon="terminal">
    Every command has built-in help with fields, types, and examples.
  </Card>

  <Card title="Zero dependencies" icon="feather">
    A single ESM bundle on Node.js 22+. Zero runtime dependencies.
  </Card>
</CardGroup>

## Install

```bash theme={null}
npm install -g @coinbase/cdp-cli
cdp --version
```

<Info>
  Node.js 22 or later is required.
</Info>

## What's available

Run `cdp` to see the current resources and commands.

**EVM Accounts and Solana Accounts**: create accounts, sign messages and transactions, send using the encode-sign-send pipeline, manage smart accounts ([ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)), and execute token swaps.

**Onchain Data**: token balances, SQL queries against indexed chain data, and webhook subscriptions for on-chain event monitoring.

**Policy Engine**: accept/reject rules by value, address, or network, attachable to any account.

**End User Accounts, Onramp, and x402**: embedded wallets for end users, fiat-to-crypto onramp via Coinbase, and payments over the [x402 protocol](/x402/welcome).

**Client-side utilities**: transaction encoding and decoding, ABI encoding, and key encryption. These run locally with no network calls.

## Already using the CDP SDK?

The CLI complements the SDK for workflows where a command is faster than writing code:

* **Ad-hoc operations**: create an account, check a balance, or fund a testnet wallet without opening an editor
* **Debugging**: decode a raw transaction with `cdp util tx-decode`, inspect request and response headers with `cdp api -v`
* **Exploration**: browse every endpoint with `cdp api`, preview request shapes with `‑‑template`, iterate with `--edit`
* **AI agents**: the [MCP server](/get-started/tools/cdp-cli-mcp) exposes every CDP operation as a typed tool

The CLI is self-documenting. Run `cdp evm --help` to see all actions, or `cdp evm accounts create --help` to see fields and examples for a specific action.

## Architecture

| Layer            | Description                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| **CLI**          | Commands for exploration and automation                                                          |
| **MCP server**   | Stdio-based [Model Context Protocol](https://modelcontextprotocol.io) server for AI tool-calling |
| **Agent skills** | Bundled workflows that teach assistants how to use the CLI                                       |

## Next steps

<CardGroup>
  <Card title="Quickstart" icon="rocket" href="/get-started/tools/cdp-cli-quickstart">
    Install, authenticate, and send a first testnet transaction.
  </Card>

  <Card title="How It Works" icon="book" href="/get-started/tools/cdp-cli-how-it-works">
    Credentials, environments, field syntax, and the encode-sign-send pipeline.
  </Card>

  <Card title="MCP Integration" icon="robot" href="/get-started/tools/cdp-cli-mcp">
    Typed tool access to every CDP endpoint for AI agents.
  </Card>
</CardGroup>

