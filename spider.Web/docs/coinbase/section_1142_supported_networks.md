# Supported Networks
Source: https://docs.cdp.coinbase.com/get-started/supported-networks



<link href="/supported-networks.css?v=7" />

This page provides an overview of the blockchain networks we currently support.

<Accordion title="What is a network?">
  A **network** is the blockchain infrastructure supporting transactions, dapps, and smart contracts, with its own rules, consensus mechanism, and native tokens. For example, wallets, addresses, and assets are created on a specific network.
</Accordion>

## EVM Networks

<div>
  | Tool                                                                                              | Base | Ethereum | Arbitrum | Polygon | Details                                                                                                                                                  |
  | ------------------------------------------------------------------------------------------------- | ---- | -------- | -------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | <img /> **WALLETS**                                                                               |      |          |          |         |                                                                                                                                                          |
  | [Server Wallet](/server-wallets/v2/introduction/welcome)<br />*Create & manage wallets*           | ✅    | ✅        | ✅        | ✅       | Supports **all EVM networks**                                                                                                                            |
  | [Embedded Wallet](/embedded-wallets/welcome)<br />*In-app wallets with email login*               | ✅    | ✅        | ✅        | ✅       | Supports **all EVM networks**                                                                                                                            |
  | <img /> **PAYMENTS**                                                                              |      |          |          |         |                                                                                                                                                          |
  | [Send & Receive](/server-wallets/v2/using-the-wallet-api/transfers)<br />*Transfer crypto assets* | ✅    | ✅        | ✅        | ✅       | Supports **all EVM networks**                                                                                                                            |
  | [Onramp](/onramp/introduction/welcome)<br />*Fiat to crypto conversion*                           | ✅    | ✅        | ✅        | ✅       | • Support for > 50 networks<br />• Varies by location. [Check availability](https://onramp-asset-availability.vercel.app/)                               |
  | [x402](/x402/welcome)<br />*Micropayment protocol*                                                | ✅    | ✅        | ✅        | ✅       | • CDP [Facilitator](/x402/core-concepts/facilitator): **Base**<br />• Self-hosted Facilitator: **any EVM network**                                       |
  | <img /> **SWAPS**                                                                                 |      |          |          |         |                                                                                                                                                          |
  | [Trade API](/trade-api/welcome)<br />*Token swapping*                                             | ✅    | ✅        | ❌        | ❌       | **Mainnet** only                                                                                                                                         |
  | <img /> **BASE TOOLS**                                                                            |      |          |          |         |                                                                                                                                                          |
  | [Paymaster](/paymaster/introduction/welcome)<br />*Gas sponsorship*                               | ✅    | ❌        | ❌        | ❌       |                                                                                                                                                          |
  | <img /> **DATA**                                                                                  |      |          |          |         |                                                                                                                                                          |
  | [Node](/data/node/overview)<br />*RPC endpoints*                                                  | ✅    | ❌        | ❌        | ❌       |                                                                                                                                                          |
  | [Webhooks](/data/webhooks/overview)<br />*Real-time events*                                       | ✅    | ❌        | ❌        | ❌       |                                                                                                                                                          |
  | <img /> **AI**                                                                                    |      |          |          |         |                                                                                                                                                          |
  | [AgentKit](/agent-kit/welcome)<br />*AI-powered agents*                                           | ✅    | ✅        | ✅        | ✅       | • Network availability depends on [wallet provider config](https://docs.cdp.coinbase.com/agent-kit/core-concepts/wallet-management#wallet-configuration) |
  | <img /> **STAKING**                                                                               |      |          |          |         |                                                                                                                                                          |
  | [Staking API](/staking/staking-api/introduction/welcome)<br />*Programmatic staking*              | ❌    | ✅        | ❌        | ❌       |                                                                                                                                                          |
  | <img /> **FAUCET**                                                                                |      |          |          |         |                                                                                                                                                          |
  | [Faucets](/faucets/introduction/welcome)<br />*Test tokens*                                       | ✅    | ✅        | ❌        | ❌       | **Testnet** only                                                                                                                                         |
</div>

## Non-EVM Networks

<div>
  | Tool                                                                                              | Bitcoin | Solana | Details                                                                                                                                                  |
  | ------------------------------------------------------------------------------------------------- | ------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | <img /> **WALLETS**                                                                               |         |        |                                                                                                                                                          |
  | [Server Wallet](/server-wallets/v2/introduction/welcome)<br />*Create & manage wallets*           | ❌       | ✅      |                                                                                                                                                          |
  | [Embedded Wallet](/embedded-wallets/welcome)<br />*In-app wallets with email login*               | ❌       | ✅      |                                                                                                                                                          |
  | <img /> **PAYMENTS**                                                                              |         |        |                                                                                                                                                          |
  | [Send & Receive](/server-wallets/v2/using-the-wallet-api/transfers)<br />*Transfer crypto assets* | ❌       | ✅      |                                                                                                                                                          |
  | [Onramp](/onramp/introduction/welcome)<br />*Fiat to crypto conversion*                           | ✅       | ✅      | • Support for > 50 networks<br />• Varies by location. [Check availability](https://onramp-asset-availability.vercel.app/)                               |
  | [x402](/x402/welcome)<br />*Micropayment protocol*                                                | ❌       | ❌      | **Solana** support in development                                                                                                                        |
  | <img /> **DATA**                                                                                  |         |        |                                                                                                                                                          |
  | [Token Balances](/data/token-balance/welcome)<br />*Query token balances*                         | ❌       | ✅      | **Beta**                                                                                                                                                 |
  | <img /> **AI**                                                                                    |         |        |                                                                                                                                                          |
  | [AgentKit](/agent-kit/welcome)<br />*AI-powered agents*                                           | ❌       | ✅      | • Network availability depends on [wallet provider config](https://docs.cdp.coinbase.com/agent-kit/core-concepts/wallet-management#wallet-configuration) |
  | <img /> **STAKING**                                                                               |         |        |                                                                                                                                                          |
  | [Staking API](/staking/staking-api/introduction/welcome)<br />*Programmatic staking*              | ❌       | ✅      |                                                                                                                                                          |
  | <img /> **FAUCET**                                                                                |         |        |                                                                                                                                                          |
  | [Faucets](/faucets/introduction/welcome)<br />*Test tokens*                                       | ❌       | ✅      | **Testnet** only                                                                                                                                         |
</div>

## Use cases

<Accordion title="Mainnets vs. Testnets">
  * **Mainnet:** Live, fully operational blockchain with real transactions and actual assets
  * **Testnets:** Sandbox environments for testing smart contracts, dapps, and other blockchain functionality without risking real funds. You can obtain test currencies from [faucets](/faucets/introduction/welcome)

  For example:

  | **Testnet**                                                                                                                           | **Mainnet**      |
  | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
  | [Base-Sepolia](https://docs.base.org/chain/network-information#base-testnet-sepolia)                                                  | Base-Mainnet     |
  | [Ethereum-Sepolia](https://ethereum.org/en/developers/docs/networks/#sepolia), [Ethereum-Hoodi](https://github.com/eth-clients/hoodi) | Ethereum-Mainnet |
  | [Solana-Devnet](https://solana.com/docs/references/clusters#devnet)                                                                   | Solana-Mainnet   |
</Accordion>

### Mainnets

Use mainnets for production-grade transactions and interactions using CDP APIs:

* Sending real crypto funds (e.g., withdrawals, payments)
* Interacting with live DeFi protocols (such as staking)
* Reading onchain data for dashboards, analytics, etc.

CDP APIs can help simplify production workflows by letting you query balances, transactions, or fetch events without running a node.

### Testnets

Use testnets for development, testing, or QA with no real funds involved:

* Testing smart contract deployments before mainnet launch
* Simulating workflows (like login, staking, etc.) with testnet funds
* Continuous Integration tests that run contract calls
* Demo purposes for sandbox environments

### Layer 2s

Use Layer 2s, such as the Base network, for lower fees and faster transactions:

* Powering gas-efficient wallets or dapps
* Game or social app activity (frequent, low-cost interactions)
* Bridging assets between networks

## What to read next

* [Authentication](/get-started/authentication/cdp-api-keys): Set up API keys for CDP
* [Quickstart](/get-started/quickstart): Build your first onchain app
* [Demo Apps](/get-started/demo-apps/explore): Explore sample applications

