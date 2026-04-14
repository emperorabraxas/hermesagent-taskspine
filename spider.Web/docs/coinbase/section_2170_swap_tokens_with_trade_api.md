# Swap tokens with Trade API
Source: https://docs.cdp.coinbase.com/server-wallets/v2/evm-features/swaps



## Overview

The Server Wallet provides a convenient way to execute swaps using CDP EVM accounts. This feature combines the core Trade APIs (which handle price discovery and quote creation) with the Server Wallet's ability to sign and broadcast transactions.

<Note>
  For detailed information about the core Trade APIs (price discovery and quote creation), see the [Trade APIs documentation](/trade-api/welcome).
</Note>

<Info>
  The Trade API currently supports Ethereum, Base, Arbitrum, Optimism and Polygon mainnet networks only. Additional network support will be added in future updates.
</Info>

## Prerequisites

It is assumed you have already completed the Server Wallet [Quickstart](/server-wallets/v2/introduction/quickstart) guide and have a CDP account ready to use.

## Using CDP Accounts

When using CDP EVM [Accounts](/server-wallets/v2/introduction/accounts), we offer two options for submitting swaps:

1. **All-in-one swap** (recommended): Submit a swap in one call
2. **Quote, then swap** (advanced): Create a quote first, then execute the swap. This is useful for detailed swap inspection or custom logic.

<Note>
  These actions may reserve funds onchain, and are strictly rate-limited.
</Note>

## Code Examples

For complete code examples showing how to execute swaps with both regular accounts (EOAs) and Smart Accounts using CDP Wallets, see the [Trade API Quickstart guide](/trade-api/quickstart):

* **[Regular Accounts (EOAs)](/trade-api/quickstart#regular-accounts-eoas)** - Price estimation, creating quotes, and executing swaps with standard accounts
* **[Smart Accounts](/trade-api/quickstart#smart-accounts)** - Leveraging ERC-4337 features like gas sponsorship and batch operations

The quickstart guide includes examples in both TypeScript and Python, along with links to full implementations on GitHub.

## What to read next

* [**Trade API Documentation**](/trade-api/welcome): Learn more about the core Trade APIs for price discovery and quote creation
* [**Quickstart Guide**](/trade-api/quickstart): Step-by-step examples for implementing swaps
* [**Smart Accounts**](/server-wallets/v2/evm-features/smart-accounts): Learn about using ERC-4337 Smart Accounts for advanced features

