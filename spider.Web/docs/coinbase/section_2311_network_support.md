# Network Support
Source: https://docs.cdp.coinbase.com/x402/network-support



x402 supports multiple blockchain networks for payment processing. This page covers what the x402 reference SDKs support, what the CDP facilitator is configured for, and where to find other facilitators.

## Network Identifiers (CAIP-2)

x402 v2 uses [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md) (Chain Agnostic Improvement Proposal) format for network identifiers. This provides a standardized way to identify blockchain networks across the ecosystem.

### CAIP-2 Format

The format is: `namespace:reference`

* **EVM Networks**: `eip155:{chainId}` where `chainId` is the EVM chain ID
* **Solana Networks**: `solana:{genesisHash}` where `genesisHash` is a truncated genesis hash

### Examples

```typescript theme={null}
// EVM networks
network: "eip155:8453"      // Base mainnet (chain ID 8453)
network: "eip155:84532"     // Base Sepolia (chain ID 84532)
network: "eip155:137"       // Polygon mainnet (chain ID 137)
network: "eip155:1"         // Ethereum mainnet (chain ID 1)

// Solana networks
network: "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"  // Solana mainnet
network: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1"  // Solana devnet
```

## Reference SDK Support

The x402 reference SDKs are designed to be flexible and extensible:

### EVM Support (`@x402/evm`)

The `@x402/evm` package supports **any EVM-compatible chain** you configure and **all ERC-20 tokens** via two transfer methods:

* **EIP-3009 (Transfer With Authorization):** For tokens that natively implement [EIP-3009](https://eips.ethereum.org/EIPS/eip-3009), such as USDC and EURC. The buyer signs an off-chain authorization and the facilitator submits the transfer — no on-chain approval needed.
* **Permit2:** For **any ERC-20 token**, using [Permit2](https://github.com/Uniswap/permit2) as a universal token approval mechanism. The buyer signs a `PermitWitnessTransferFrom` message and the facilitator executes the transfer.

This includes:

* Any Ethereum L1 or L2
* Any EVM-compatible chain with a valid chain ID
* Any ERC-20 token (via Permit2) or EIP-3009 compliant token (USDC, EURC, etc.)

#### Permit2 Approval

Permit2 requires the buyer to have an active approval from the payment token to the [Permit2 contract](https://github.com/Uniswap/permit2). x402 supports two **gas sponsorship extensions** that handle this approval automatically:

* **EIP-2612 gas sponsoring:** For tokens that implement [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) (permit), the facilitator can sponsor the Permit2 approval on-chain using a signed off-chain permit message — no gas required from the buyer.
* **ERC-20 gas sponsoring:** For generic ERC-20 tokens without EIP-2612 support, the facilitator can sponsor the Permit2 approval transaction on the buyer's behalf.

Without a gas sponsorship extension, the buyer must perform a **one-time manual approval** of the payment token to the Permit2 contract before making their first payment.

<Note>
  EIP-3009 and Permit2 (including gas sponsorship extensions) are supported in the official **TypeScript** (`@x402/evm`), **Go**, and **Python** SDKs.
</Note>

### Solana Support (`@x402/svm`)

The `@x402/svm` package supports **any Solana cluster** with:

* SPL Token Program tokens
* Token2022 program tokens

### Other SDKs

Community and third-party SDKs may expand support to other protocol families or chains beyond what the reference SDKs currently support. Check the [x402 ecosystem](https://www.x402.org/ecosystem) for additional implementations.

## CDP Facilitator Support

The CDP (Coinbase Developer Platform) facilitator is our recommended choice for both testnet and mainnet. It supports the following networks and schemes:

| Network       | CAIP-2 Identifier                         | v1 Support | v2 Support | Scheme          | Pricing     |
| ------------- | ----------------------------------------- | ---------- | ---------- | --------------- | ----------- |
| Base          | `eip155:8453`                             | ✅          | ✅          | `exact`, `upto` | Free tier\* |
| Base Sepolia  | `eip155:84532`                            | ✅          | ✅          | `exact`, `upto` | Free tier\* |
| Polygon       | `eip155:137`                              | ✅          | ✅          | `exact`, `upto` | Free tier\* |
| Solana        | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | ✅          | ✅          | `exact`         | Free tier\* |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | ✅          | ✅          | `exact`         | Free tier\* |

\*1,000 transactions free per month, then \$0.001/transaction. Gas is paid on-chain separately. See [Facilitator Pricing](/x402/core-concepts/facilitator#pricing) for details.

**CDP Facilitator Endpoints:**

* **Mainnet**: `https://api.cdp.coinbase.com/platform/v2/x402`
  * Requires CDP API keys
  * Supports: Base, Polygon, Solana

## x402.org Testnet Facilitator

For testnet-only use without CDP signup, the x402.org facilitator is available:

| Network       | CAIP-2 Identifier                         | v1 Support | v2 Support | Scheme          |
| ------------- | ----------------------------------------- | ---------- | ---------- | --------------- |
| Base Sepolia  | `eip155:84532`                            | ✅          | ✅          | `exact`, `upto` |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | ✅          | ✅          | `exact`         |

**Endpoint**: `https://x402.org/facilitator`

* No API key required
* For testnet use only

## Other Facilitators

The x402 protocol is permissionless, so anyone can run a facilitator. The ecosystem includes several community and third-party facilitators that support additional networks, tokens, and features.

<Info>
  For a complete and up-to-date list of facilitators, visit the [x402 Ecosystem](https://www.x402.org/ecosystem?category=facilitators).
</Info>

## Chain ID Reference

Quick reference for common EVM chain IDs:

| Chain ID | Network           | CAIP-2 Format  |
| -------- | ----------------- | -------------- |
| 1        | Ethereum Mainnet  | `eip155:1`     |
| 10       | Optimism          | `eip155:10`    |
| 137      | Polygon           | `eip155:137`   |
| 8453     | Base              | `eip155:8453`  |
| 84532    | Base Sepolia      | `eip155:84532` |
| 42161    | Arbitrum One      | `eip155:42161` |
| 43114    | Avalanche C-Chain | `eip155:43114` |
| 43113    | Avalanche Fuji    | `eip155:43113` |

## Token Support

### EVM Networks

On EVM networks, x402 supports **all ERC-20 tokens** via two transfer methods:

* **EIP-3009 tokens** (e.g., USDC, EURC): Use [EIP-3009](https://eips.ethereum.org/EIPS/eip-3009) (Transfer With Authorization) for fully gasless transfers where the buyer signs an off-chain message and the facilitator submits the transaction. No on-chain approval step is needed.
* **Generic ERC-20 tokens:** Use [Permit2](https://github.com/Uniswap/permit2) for transfers. The buyer must have an approval to the Permit2 contract, which can be handled via gas sponsorship extensions (EIP-2612 or ERC-20 gas sponsoring) or a one-time manual approval.

**Common EIP-3009 Tokens:**

| Token | Base                                         | Base Sepolia                                 | Polygon                                      |
| ----- | -------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| USDC  | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` |

<Note>
  Any ERC-20 token can be used with x402 via Permit2. EIP-3009 compliant tokens like USDC provide the smoothest experience since they require no on-chain approval. The token addresses above are the most commonly used with the CDP facilitator.
</Note>

### Solana Networks (SPL / Token2022)

On Solana, x402 supports SPL Token Program tokens for v1 and v2, and Token2022 program tokens for v2 only.

**Common Tokens:**

| Token | Mainnet                                        | Devnet             |
| ----- | ---------------------------------------------- | ------------------ |
| USDC  | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | (faucet available) |

## Price Formatting

x402 supports multiple price formats for convenience:

```typescript theme={null}
// Dollar string format (recommended for readability)
price: "$0.001"    // 0.001 USDC
price: "$1.00"     // 1 USDC
price: "$0.50"     // 0.50 USDC

// Atomic units (for precision)
amount: "1000"     // 0.001 USDC (6 decimals)
amount: "1000000"  // 1 USDC (6 decimals)
```

## Usage Examples

### Server-Side Configuration

<Tabs>
  <Tab title="Node.js">
    ```typescript theme={null}
    import { paymentMiddleware, x402ResourceServer } from "@x402/express";
    import { ExactEvmScheme } from "@x402/evm/exact/server";
    import { HTTPFacilitatorClient } from "@x402/core/server";

    const facilitatorClient = new HTTPFacilitatorClient({
      url: "https://x402.org/facilitator",
    });

    // Register scheme for Base Sepolia
    const server = new x402ResourceServer(facilitatorClient)
      .register("eip155:84532", new ExactEvmScheme());

    app.use(
      paymentMiddleware(
        {
          "GET /api": {
            accepts: [
              {
                scheme: "exact",
                price: "$0.001",
                network: "eip155:84532", // Base Sepolia
                payTo: "0xYourAddress",
              },
            ],
            description: "API endpoint",
          },
        },
        server,
      ),
    );
    ```
  </Tab>

  <Tab title="Go">
    ```go theme={null}
    import (
        x402 "github.com/coinbase/x402/go"
        x402http "github.com/coinbase/x402/go/http"
        evm "github.com/coinbase/x402/go/mechanisms/evm/exact/server"
    )

    network := x402.Network("eip155:84532") // Base Sepolia

    r.Use(ginmw.X402Payment(ginmw.Config{
        Routes: x402http.RoutesConfig{
            "GET /api": {
                Scheme:  "exact",
                PayTo:   payTo,
                Price:   "$0.001",
                Network: network,
            },
        },
        Facilitator: facilitatorClient,
        Schemes: []ginmw.SchemeConfig{
            {Network: network, Server: evm.NewExactEvmScheme()},
        },
    }))
    ```
  </Tab>
</Tabs>

### Using a Custom Network

Since `@x402/evm` supports any EVM chain, you can configure networks not listed above:

```typescript theme={null}
// Example: Using Ethereum mainnet with a custom facilitator
const facilitatorClient = new HTTPFacilitatorClient({
  url: "https://example.facilitator.com",
});

const server = new x402ResourceServer(facilitatorClient)
  .register("eip155:1", new ExactEvmScheme()); // Ethereum mainnet

app.use(
  paymentMiddleware(
    {
      "GET /api": {
        accepts: [
          {
            scheme: "exact",
            price: "$0.001",
            network: "eip155:1",
            payTo: "0xYourAddress",
            asset: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC on Ethereum
          },
        ],
        description: "API endpoint",
      },
    },
    server,
  ),
);
```

### Multi-Network Support

Support multiple networks on the same endpoint:

```typescript theme={null}
{
  "GET /api": {
    accepts: [
      {
        scheme: "exact",
        price: "$0.001",
        network: "eip155:8453",  // Base mainnet
        payTo: "0xYourEvmAddress",
      },
      {
        scheme: "exact",
        price: "$0.001",
        network: "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",  // Solana mainnet
        payTo: "YourSolanaAddress",
      },
    ],
    description: "Multi-network endpoint",
  },
}
```

## Running Your Own Facilitator

If you need to support networks or tokens not available through existing facilitators, you can run your own:

1. **Use the reference implementation**: The [x402 GitHub repository](https://github.com/coinbase/x402) contains facilitator code
2. **Use a community implementation**: Check the [x402 Ecosystem](https://www.x402.org/ecosystem?category=facilitators) for self-hostable options

## Next Steps

* [Quickstart for Sellers](/x402/quickstart-for-sellers) - Start accepting payments
* [Quickstart for Buyers](/x402/quickstart-for-buyers) - Start making payments
* [Core Concepts: Facilitator](/x402/core-concepts/facilitator) - Learn about facilitators
* [x402 Ecosystem](https://www.x402.org/ecosystem) - Explore facilitators and tools

