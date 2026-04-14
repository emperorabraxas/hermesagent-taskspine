# Quickstart for Buyers
Source: https://docs.cdp.coinbase.com/x402/quickstart-for-buyers



<Info>
  Need help? Join the [x402 Discord](https://discord.gg/cdp) for the latest
  updates.
</Info>

## Facilitator URLs

| Environment             | Facilitator URL                                 | Networks                                           | Auth                  |
| ----------------------- | ----------------------------------------------- | -------------------------------------------------- | --------------------- |
| **CDP (recommended)**   | `https://api.cdp.coinbase.com/platform/v2/x402` | Base, Base Sepolia, Polygon, Solana, Solana Devnet | CDP API keys required |
| x402.org (testnet only) | `https://x402.org/facilitator`                  | Base Sepolia, Solana Devnet                        | None                  |

We recommend the CDP facilitator for both testnet and mainnet. Use x402.org if you want to try x402 without signing up.

This guide walks you through how to use **x402** to interact with services that require payment. By the end of this guide, you will be able to programmatically discover payment requirements, complete a payment, and access a paid resource.

The x402 helper packages for various languages greatly simplify your integration with x402. You'll be able to automatically detect payment challenges, authorize payments onchain, and retry requests with minimal code. The packages will automatically trigger the following flow:

1. Makes the initial request (if using Fetch) or intercepts the initial request (if using Axios)
2. If a 402 response is received, parses the payment requirements from the `PAYMENT-REQUIRED` header
3. Creates a payment payload using the configured x402Client and registered schemes
4. Retries the request with the `PAYMENT-SIGNATURE` header

## Prerequisites

Before you begin, ensure you have:

* A crypto wallet with USDC (any EVM-compatible wallet, e.g., [CDP Wallet](/server-wallets/v2/introduction/quickstart), [AgentKit](/agent-kit/welcome))
* [Node.js](https://nodejs.org/en) and npm, [Go](https://go.dev/), or Python and pip installed
* A service that requires payment via x402
* **For testnet:** Base Sepolia ETH for gas and testnet USDC. Get funds from the [CDP Faucet](/faucets/introduction/quickstart)

<Info>
  We have pre-configured [examples available in our
  repo](https://github.com/coinbase/x402/tree/main/examples), including examples
  for fetch, Axios, and MCP.
</Info>

## 1. Install Dependencies

<Tabs>
  <Tab title="Node.js">
    Install the x402 client packages:

    ```bash theme={null}
    # For fetch-based clients
    npm install @x402/fetch @x402/evm

    # For axios-based clients
    npm install @x402/axios @x402/evm

    # For Solana support, also add:
    npm install @x402/svm

    # For Bazaar discovery (optional):
    npm install @x402/core @x402/extensions
    ```
  </Tab>

  <Tab title="Go">
    Add the x402 Go module to your project:

    ```bash theme={null}
    go get github.com/coinbase/x402/go
    ```
  </Tab>

  <Tab title="Python">
    Install the [x402 package](https://pypi.org/project/x402/) with your preferred HTTP client:

    ```bash theme={null}
    # For httpx (async) - recommended
    pip install "x402[httpx]"

    # For requests (sync)
    pip install "x402[requests]"

    # For Solana support, also add:
    pip install "x402[svm]"
    ```
  </Tab>
</Tabs>

## 2. Create a Wallet Client

Create a wallet client using CDP's [Server Wallet](/server-wallets/v2/introduction/quickstart) (recommended) or a standalone wallet library ([viem](https://viem.sh/) for EVM on Node.js, or Go's crypto libraries).

<Tip>
  **Building with Embedded Wallets?** If you're building a user-facing
  application with embedded wallets, check out the [X402 with Embedded
  Wallets](/embedded-wallets/x402-payments) guide which shows how to use the
  `useX402` hook for seamless payment integration.
</Tip>

### CDP Server Wallet (Recommended)

First, create an account at [cdp.coinbase.com](https://cdp.coinbase.com/) and get the following API keys from the portal to store as environment variables:

```bash theme={null}