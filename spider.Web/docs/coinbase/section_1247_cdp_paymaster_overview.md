# CDP Paymaster Overview
Source: https://docs.cdp.coinbase.com/paymaster/introduction/welcome



## What is Gas Sponsorship?

On Ethereum and EVM-compatible blockchains, every transaction requires **gas**—a fee paid in ETH to compensate the network for processing your transaction. This creates friction for new users who need to acquire ETH before they can do anything onchain.

**Gas sponsorship** solves this by letting developers pay gas fees on behalf of their users. Instead of users needing ETH in their wallet, your application covers the cost. This creates a seamless, "gasless" experience similar to traditional web apps.

## How Paymasters Work

A **Paymaster** is a smart contract that sponsors gas fees for user transactions. It's a core component of [ERC-4337 Account Abstraction](https://eips.ethereum.org/EIPS/eip-4337), which enables programmable transaction flows beyond what traditional EOA (Externally Owned Account) wallets can do.

Here's the flow:

1. **User initiates a transaction** from a smart account (not an EOA)
2. **Bundler receives the userOperation** and checks if a Paymaster will sponsor it
3. **Paymaster evaluates the request** against your configured policies (allowlisted contracts, spend limits, etc.)
4. **If approved, the Paymaster pays the gas** and the transaction executes
5. **You're billed** for the sponsored gas plus a 7% fee through your CDP account (monthly invoicing)

<Note>
  Gas sponsorship only works with **smart accounts** (ERC-4337), not traditional EOAs. With EIP-7702, EOAs can be upgraded to smart accounts to enable sponsorship. See the [EIP-7702 FAQs](/paymaster/faqs#eip-7702) for details.
</Note>

## CDP Paymaster

The Coinbase Developer Platform Paymaster provides a fully-managed gas sponsorship service that includes:

* **Paymaster + Bundler in one endpoint** — A single API endpoint handles both paymaster signing and transaction bundling
* **Policy controls** — Configure contract allowlists, per-user limits, and global spend caps
* **Analytics & logs** — Monitor sponsored transactions, gas usage, and costs
* **ERC-7677 compliant** — Works with any compatible SDK or wallet (does not have to be paired with CDP Wallets)

### Supported Networks

<Warning>
  CDP Paymaster currently supports **Base Mainnet** and **Base Sepolia** only.

  For other EVM networks, you can use any [ERC-7677 compliant](https://www.erc7677.xyz/ecosystem/paymasters) paymaster provider with CDP Smart Accounts.
</Warning>

| Network            | Status                              |
| ------------------ | ----------------------------------- |
| Base Mainnet       | ✅ Supported                         |
| Base Sepolia       | ✅ Supported                         |
| Other EVM networks | Use third-party ERC-7677 paymasters |

## Get Started

<Steps>
  <Step title="Create a CDP account">
    [Sign up](https://coinbase.com/developer-platform) for CDP or [sign in](https://portal.cdp.coinbase.com) to your existing account.
  </Step>

  <Step title="Get your Paymaster endpoint">
    Navigate to [Paymaster](https://portal.cdp.coinbase.com/products/bundler-and-paymaster) under **Onchain Tools** in the left-nav. Copy your endpoint URL.
  </Step>

  <Step title="Configure your gas policy">
    Set up a contract allowlist to control which contracts you'll sponsor transactions for. This protects against unintended sponsorship.
  </Step>

  <Step title="Integrate with your app">
    Follow the [Quickstart](/paymaster/introduction/quickstart) to integrate gas sponsorship into your application.
  </Step>

  <Step title="Apply for gas credits">
    [Apply for up to \$15K in gas credits](https://docs.google.com/forms/d/1yPnBFW0bVUNLUN_w3ctCqYM9sjdIQO3Typ53KXlsS5g/viewform?edit_requested=true\&pli=1) as part of the Base Gasless Campaign.
  </Step>
</Steps>

## Example Repository

See [our examples on GitHub](https://github.com/coinbase/paymaster-bundler-examples) for integrations with popular SDKs including Viem, Permissionless, and more.

## Need Help?

Reach out in the `#paymaster` channel in the [CDP Discord](https://discord.com/invite/cdp).

