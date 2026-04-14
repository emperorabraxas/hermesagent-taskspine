# Smart Accounts
Source: https://docs.cdp.coinbase.com/embedded-wallets/evm-features/smart-accounts



## Overview

Smart accounts ([ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)) are programmable wallets that enable advanced features like batching multiple transactions together and sponsoring gas fees for your users.

Key benefits of CDP Smart Accounts include:

<CardGroup>
  <Card title="Batch transactions" icon="layer-group" href="#batch-calls">
    Execute multiple calls in a single user operation
  </Card>

  <Card title="Gas sponsorship" icon="gas-pump" href="#gas-sponsorship-with-paymaster">
    Optional paymasters for gasless UX
  </Card>

  <Card title="Multi-chain support" icon="network-wired" href="#using-non-base-networks">
    Deploy on 8 mainnets and 2 testnets across EVM chains
  </Card>
</CardGroup>

This guide shows how to enable smart accounts in Embedded Wallets, send user operations, and integrate a paymaster.

<Tip>
  If you're new to Embedded Wallets, start with the [Quickstart](/embedded-wallets/quickstart) and [React Hooks](/embedded-wallets/react-hooks) first.
</Tip>

<Note>
  **Prefer keeping the same address?** [EIP-7702 delegation](/embedded-wallets/evm-features/eip-7702-delegation) gives a user's existing EOA the same smart account capabilities — batched transactions, gas sponsorship, and spend permissions — without creating a new contract address. Unlike ERC-4337 which issues a separate contract account, EIP-7702 upgrades the EOA in place so the address never changes.
</Note>

<Note>
  Embedded Wallets do not support the Policy Engine. Embedded Wallets can use [Paymaster allowlists](/paymaster/introduction/welcome) today; Smart Account spend permissions are coming soon.
</Note>

## Prerequisites

* A CDP Portal account and project
* Node.js 22+ and a package manager (npm, pnpm, or yarn)
* Basic familiarity with React and TypeScript
* A CDP project with Embedded Wallets enabled
* Your app domain [allowlisted](/embedded-wallets/domains)
* `@coinbase/cdp-core` and `@coinbase/cdp-hooks` installed

```bash theme={null}