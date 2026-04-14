# Custom Stablecoins
Source: https://docs.cdp.coinbase.com/custom-stablecoins/overview



Custom Stablecoins allow companies to hold customer or corporate balances in their own branded token and earn revenue on every dollar in circulation.

Each token is backed 1:1 by USDC on Coinbase, fully interoperable with USDC and deployable on Base, Solana or any EVM-compatible network.

This documentation is for **technical partners** integrating with Custom Stablecoins. You can swap tokens directly onchain via the [Stableswapper](/custom-stablecoins/quickstart) program, or use the [Prime API](/custom-stablecoins/prime-conversions) for centralized conversions and withdrawals through Coinbase Prime.

## Use cases

<CardGroup>
  <Card title="Payments" icon="money-bill-wave">
    Power branded payments across your app, platform, or merchant network. Fully backed and instantly redeemable for USDC.
  </Card>

  <Card title="Loyalty and rewards" icon="gift">
    Hold customer balances in your branded stablecoin, earn rewards on circulating supply and put that revenue back into user incentives or cashback.
  </Card>

  <Card title="Treasury" icon="building-columns">
    Run internal settlements and B2B payments while generating revenue on your circulating supply.
  </Card>

  <Card title="DeFi protocols" icon="chart-line">
    Integrate a custom stablecoin into your protocol with instant USDC liquidity for users.
  </Card>
</CardGroup>

## Key features

* **1:1 USDC backing**: Fully backed by USDC reserves on Coinbase
* **Instant swaps**: Single-transaction settlement
* **Predictable pricing**: Fixed 1:1 ratio with no slippage surprises
* **Multi-chain support**: Available on SVM chains (Solana) and EVM chains (Base) today, with additional chain support available on request
* **Flexible integration**: Use via Cross-Program Invocation (SVM chains) or direct smart contract calls (EVM chains)
* **Multi-decimal support**: Automatic normalization between tokens with different decimal precision
* **Prime API support**: Convert and withdraw custom stablecoins programmatically via Coinbase Prime

## Supported networks

Solana (SVM) and Base (EVM) are supported today. Additional SVM and EVM chains are available on request — contact Coinbase to discuss support for your preferred network.

| Network        | VM type | Use case                | Contract type      |
| -------------- | ------- | ----------------------- | ------------------ |
| Solana Devnet  | SVM     | Testing and development | Anchor program     |
| Solana Mainnet | SVM     | Production use          | Anchor program     |
| Base Sepolia   | EVM     | Testing and development | EVM smart contract |
| Base Mainnet   | EVM     | Production use          | EVM smart contract |

## Onchain conversions

Stableswapper is the onchain liquidity program that powers instant swaps between USDC and any Custom Stablecoin issued through the program. It is deployed on both **SVM chains (Solana)** and **EVM chains (Base)**, providing the settlement layer partners need to let their users move freely between custom tokens and USDC. Learn how to [integrate swaps](/custom-stablecoins/quickstart) into your application.

### How it works

The Stableswapper program maintains a **liquidity pool** with reserves for each supported token.

<Steps>
  <Step title="User initiates swap">
    The input token is transferred to the contract
  </Step>

  <Step title="Validation">
    The program checks the allowlist (if enabled), validates slippage protection, and applies any configured fee
  </Step>

  <Step title="Settlement">
    The equivalent amount of the output token is sent to the destination address
  </Step>
</Steps>

Swaps settle atomically in a single transaction at a **1:1 ratio before fees**, with automatic decimal normalization between tokens with different precision.

### Concepts

<Tabs>
  <Tab title="Solana Virtual Machine">
    | Concept                            | Description                                                                                                                          |
    | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
    | **PDA** (Program Derived Address)  | Deterministic on-chain account owned by the program — used for the pool, vaults, and whitelist                                       |
    | **Vault**                          | A PDA that acts as the logical owner for a token's reserves within the pool                                                          |
    | **Vault Token Account**            | The SPL token account that actually holds the token reserves for a given vault                                                       |
    | **ATA** (Associated Token Account) | A user's standard token account for a given mint, derived deterministically from their wallet                                        |
    | **Whitelist**                      | An optional on-chain list of authorized wallet addresses. When enabled, only listed addresses can execute swaps                      |
    | **Slippage**                       | The minimum acceptable output amount (`min_amount_out`). Protects against fee changes between transaction construction and execution |
  </Tab>

  <Tab title="Ethereum Virtual Machine">
    | Concept                   | Description                                                                                                                        |
    | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
    | **ERC-20**                | The standard token interface used by all supported stablecoins on Base                                                             |
    | **Allowlist**             | An optional on-chain list of authorized addresses. When enabled, only allowlisted addresses can initiate swaps                     |
    | **Fee basis points**      | Swap fee expressed in basis points (1 bp = 0.01%)                                                                                  |
    | **Decimal normalization** | Automatic conversion between tokens with different decimal precision (e.g., 6 vs 18 decimals)                                      |
    | **Slippage**              | The minimum acceptable output amount (`minAmountOut`). Protects against fee changes between transaction construction and execution |
  </Tab>
</Tabs>

## Prime conversions

Partners with Coinbase Prime accounts can convert between USDC and custom stablecoins using the Prime Conversion API, and withdraw converted tokens to onchain wallets. This path is ideal for institutional workflows and Prime-custodied assets. Learn more in the [Prime Conversions](/custom-stablecoins/prime-conversions) guide.

## What to read next

<CardGroup>
  <Card title="Quickstart" icon="rocket" href="/custom-stablecoins/quickstart">
    Get up and running with your first swap in 10 minutes
  </Card>

  <Card title="Reference" icon="book" href="/custom-stablecoins/reference">
    Swap instruction parameters and accounts
  </Card>

  <Card title="Production Readiness" icon="shield-check" href="/custom-stablecoins/production-readiness">
    Helper functions, error handling, and best practices
  </Card>

  <Card title="Key Addresses" icon="location-dot" href="/custom-stablecoins/key-addresses">
    Program IDs, contract addresses, and token mints
  </Card>

  <Card title="Prime API" icon="arrows-rotate" href="/custom-stablecoins/prime-conversions">
    Convert and withdraw custom stablecoins via Coinbase Prime
  </Card>
</CardGroup>

