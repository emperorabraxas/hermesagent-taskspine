# @coinbase/cdp-solana-standard-wallet

A React hook and wallet implementation that integrates CDP (Coinbase Developer Platform) embedded Solana wallets with the [Wallet Standard](https://github.com/wallet-standard/wallet-standard).

## Features

* 🔗 **Wallet Standard Integration** - Works with any dapp that supports the wallet standard
* 🔐 **CDP Authentication** - Uses CDP's secure embedded wallet infrastructure
* ⚛️ **React Hooks** - Easy-to-use hooks for React applications
* 🎯 **TypeScript Support** - Full type safety with TypeScript
* 🚀 **Auto-Registration** - Automatically registers with wallet standard ecosystem
* 🔄 **Event-Driven** - Real-time updates via CDP auth state changes
* 📱 **Multi-Network** - Supports both Solana mainnet and devnet

## Installation

```bash theme={null}
npm install @coinbase/cdp-solana-standard-wallet
```

### Peer Dependencies

```bash theme={null}
npm install @coinbase/cdp-core react @wallet-standard/app @wallet-standard/base @wallet-standard/features @solana/wallet-standard bs58
```

### Optional Dependencies

Depending on your usage pattern, you may also need:

```bash theme={null}