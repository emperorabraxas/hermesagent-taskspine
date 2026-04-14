# FAQ
Source: https://docs.cdp.coinbase.com/x402/support/faq



<Info>
  Need help? Join the [x402 Discord](https://discord.gg/cdp) for the latest updates.
</Info>

## General

### What *is* x402 in a single sentence?

x402 is an open-source protocol that turns the dormant HTTP `402 Payment Required` status code into a fully-featured, on-chain payment layer for APIs, websites, and autonomous agents.

### Why not use traditional payment rails or API keys?

Traditional rails require credit-card networks, user accounts, and multi-step UI flows.
x402 removes those dependencies, enabling programmatic, HTTP-native payments (perfect for AI agents) while dropping fees to near-zero and settling in \~1 second.

### Is x402 only for crypto-native projects?

No. Any web API or content provider (crypto or web2) can integrate x402 if it wants a lower-cost, friction-free payment path for small or usage-based transactions.

## Language & Framework Support

### What languages and frameworks are supported?

**Fully Supported (v2):**

* **TypeScript/Node.js**: Express, Next.js, Hono (server); Fetch, Axios (client)
* **Go**: Gin, net/http (server and client)
* **Python**: FastAPI, Flask (server); httpx, requests (client)

<Note>
  If you're using Python with the CDP SDK for wallet signing, the correct package is `cdp-sdk` (not `cdp`):

  ```bash theme={null}
  pip install cdp-sdk
  ```

  The import is `from cdp import CdpClient`.
</Note>

The x402 protocol is **open** - nothing prevents you from implementing the spec in other languages. If you're interested in building support for your favorite language, please [open an issue](https://github.com/coinbase/x402/issues) and let us know!

### What packages should I use?

| Use Case       | Package                       |
| -------------- | ----------------------------- |
| Express server | `@x402/express` + `@x402/evm` |
| Next.js server | `@x402/next` + `@x402/evm`    |
| Hono server    | `@x402/hono` + `@x402/evm`    |
| Fetch client   | `@x402/fetch` + `@x402/evm`   |
| Axios client   | `@x402/axios` + `@x402/evm`   |
| Solana support | `@x402/svm`                   |
| Go             | `github.com/coinbase/x402/go` |

## Facilitators

### Who runs facilitators today?

Coinbase Developer Platform operates the first production facilitator. The protocol, however, is **permissionless** and anyone can run a facilitator. Expect:

* Community-run facilitators for other networks or assets.
* Private facilitators for enterprises that need custom KYT / KYC flows.

### What stops a malicious facilitator from stealing funds or lying about settlement?

Every payment payload is **signed by the buyer** and settles **directly on-chain**.
A facilitator that tampers with the transaction will fail signature checks.

### Is there a free testnet facilitator if I don't want to sign up for CDP?

Yes. The x402.org facilitator at `https://x402.org/facilitator` is free and requires no API keys. It supports Base Sepolia and Solana Devnet only (testnet). Use it for quick experimentation or demos. For mainnet and production, we recommend the [CDP facilitator](/x402/core-concepts/facilitator), which supports both testnet and mainnet with a generous free tier.

## Pricing & Schemes

### How should I price my endpoint?

There is no single answer, but common patterns are:

* **Flat per-call** (e.g., `$0.001` per request) using the `exact` scheme
* **Tiered** (`/basic` vs `/pro` endpoints with different prices)
* **Up-to** (`scheme: "upto"`): The client authorizes a maximum amount but is only charged for actual usage (tokens, compute time, bandwidth, etc.). Available on EVM networks in TypeScript and Go. See the [Seller Quickstart](/x402/quickstart-for-sellers#payment-schemes-exact-vs-upto) for setup.

### Can I integrate x402 with a usage / plan manager like Metronome?

Yes. x402 handles the **payment execution**. You can still meter usage, aggregate calls, or issue prepaid credits in Metronome and only charge when limits are exceeded. Example glue code is coming soon.

## Assets, Networks & Fees

### Which assets and networks are supported today?

**CDP Facilitator supports all ERC-20 tokens** on EVM networks via two transfer methods:

* **EIP-3009** for tokens like USDC and EURC (fully gasless, no approval needed)
* **Permit2** for any ERC-20 token (requires Permit2 approval, with optional gas sponsorship extensions)

| Network       | CAIP-2 Identifier                         | Asset                   | Pricing\* | Status  |
| ------------- | ----------------------------------------- | ----------------------- | --------- | ------- |
| Base          | `eip155:8453`                             | All ERC-20 (USDC, etc.) | Free tier | Mainnet |
| Base Sepolia  | `eip155:84532`                            | All ERC-20 (USDC, etc.) | Free tier | Testnet |
| Polygon       | `eip155:137`                              | All ERC-20 (USDC, etc.) | Free tier | Mainnet |
| Solana        | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | SPL Tokens              | Free tier | Mainnet |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | SPL Tokens              | Free tier | Testnet |

*1,000 transactions free per month, then \$0.001/transaction. Gas is paid on-chain separately. See [Facilitator Pricing](/x402/core-concepts/facilitator#pricing) for details.*

See [Network Support](/x402/network-support) for full details on transfer methods and gas sponsorship extensions.

### What is CAIP-2?

CAIP-2 (Chain Agnostic Improvement Proposal 2) is a standard format for identifying blockchain networks. x402 v2 uses this format:

* **EVM**: `eip155:{chainId}` (e.g., `eip155:8453` for Base)
* **Solana**: `solana:{genesisHash}` (e.g., `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`)

### I need support for additional networks like Avalanche. What should I do?

CDP is actively expanding network support. In the meantime:

1. Run your own facilitator - the x402 codebase supports many EVM-compatible networks including Avalanche
2. Submit a feature request through CDP support channels
3. Check the [x402 Discord](https://discord.gg/cdp) for updates on network expansion

## Security

### Do I have to expose my private key to my backend?

No. The recommended pattern is:

1. **Buyers** (clients/agents) sign locally in their runtime (browser, serverless, agent VM). You can use [CDP Server Wallet](/server-wallets/v2/introduction/quickstart) to create a programmatic wallet.
2. **Sellers** never hold the buyer's key; they only verify signatures.

### How do refunds work?

The `exact` and `upto` schemes are both **push payments** and irreversible once executed. Two options:

1. **Business-logic refunds**: Seller sends a new USDC transfer back to the buyer.
2. **Escrow schemes**: Future spec could add conditional transfers (e.g., HTLCs or hold invoices).

## Usage by AI Agents

### How does an agent know what to pay?

Agents follow the same flow as humans:

1. Make a request.
2. Parse the `PAYMENT-REQUIRED` header (base64-encoded payment requirements).
3. Choose a suitable requirement from the `accepts` array and sign a payload via the x402 client SDKs.
4. Retry with `PAYMENT-SIGNATURE` header.

### Do agents need wallets?

Yes. Programmatic wallets (e.g., **CDP Server Wallet**, `viem`, `ethers-v6` HD wallets) let agents sign payment payloads without exposing seed phrases.

## Protocol & Headers

### What headers does x402 use?

| Header              | Direction       | Purpose                                               |
| ------------------- | --------------- | ----------------------------------------------------- |
| `PAYMENT-REQUIRED`  | Server → Client | Base64-encoded payment requirements (in 402 response) |
| `PAYMENT-SIGNATURE` | Client → Server | Base64-encoded signed payment payload                 |
| `PAYMENT-RESPONSE`  | Server → Client | Settlement confirmation                               |

### How does x402 handle POST requests with request bodies?

x402 works with POST the same way as GET. The server returns 402 with `PAYMENT-REQUIRED` when payment is missing. The client signs the payment payload (the exact scope depends on the scheme — e.g., URL, method, and in some schemes the request body) and retries with `PAYMENT-SIGNATURE`. The SDKs handle POST transparently. For Bazaar discovery of POST endpoints, use `declareDiscoveryExtension` with `bodyType: "json"` and an `inputSchema` for the body. See the [Bazaar POST example](/x402/bazaar#discovery-extension-options) for the full pattern.

### What are x402 extensions?

Extensions are optional features that can be added to the x402 protocol:

* **Bazaar**: Service discovery extension for listing your API in the x402 marketplace
* **Sign-in-with-x**: Authentication extension
* **Payment Identifier**: Idempotency extension for servers or facilitators to handle duplicate calls
* **Offer Receipt**: Signed receipts tracking what was agreed upon ahead of settlement
* **EIP-2612 Gas Sponsorship**: Enables gasless Permit2 approval for tokens that implement [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612)
* **ERC-20 Gas Sponsorship**: Enables gasless Permit2 approval for generic ERC-20 tokens

Enable extensions via the `extensions` field in your route configuration.

## Governance & Roadmap

### Is there a formal spec or whitepaper?

* Spec: [GitHub Specification](https://github.com/coinbase/x402/tree/main/specs)
* [Whitepaper](https://www.x402.org/x402-whitepaper.pdf)

### How will x402 evolve?

Tracked in public GitHub issues + community RFCs. Major themes:

* Additional schemes (`stream`)
* Discovery layer for service search & reputation

### Why is x402 hosted in the Coinbase GitHub?

x402 is an open protocol developed by Coinbase in partnership with ecosystem contributors including Cloudflare. While the reference implementations currently live in the Coinbase GitHub, x402 is designed as a vendor-neutral standard. We're working toward launching an independent x402 Foundation to steward the protocol's long-term governance and development. The protocol specification, SDKs, and tooling are fully open source, and we welcome contributions from the community.

## Troubleshooting

Having issues with your x402 integration? See the dedicated [Troubleshooting Guide](/x402/support/troubleshooting) for:

* Common error messages and their solutions
* Facilitator API error codes reference
* Debugging tips and best practices

## Still have questions?

* Reach out in the [Discord channel](https://discord.gg/cdp)
* Open a GitHub Discussion or Issue in the [x402 repo](https://github.com/coinbase/x402)

