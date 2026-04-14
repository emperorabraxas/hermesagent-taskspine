# Building Miniapps with x402
Source: https://docs.cdp.coinbase.com/x402/miniapps



This guide explains how to build Farcaster Mini Apps that integrate x402 payments using our official example. The example provides a complete starting point with wallet integration, payment protection, and responsive design.

## What are Mini Apps?

Mini Apps are lightweight applications that run inside Farcaster clients. Built with [MiniKit](https://docs.base.org/builderkits/minikit/overview) and [OnchainKit](https://docs.base.org/onchainkit/latest/components/minikit/overview), they provide a native app-like experience while leveraging the social graph and wallet capabilities of Farcaster. By integrating x402, your Mini App can accept instant USDC payments without requiring users to leave the app or manage complex payment flows.

## Why x402 for Mini Apps?

x402 is particularly well-suited for Mini Apps because:

* **Seamless Payments**: Users pay without leaving the Mini App experience
* **No Account Setup**: Works directly with connected wallets
* **Instant Monetization**: Builders can monetize their content or services directly
* **Simple Integration**: Payment protection with just the `withX402` wrapper
* **No CDP API Keys Required**: Uses external facilitator directly

## Prerequisites

Before starting, ensure you have:

* Node.js 22+ and pnpm v10 installed
* USDC on Base Sepolia testnet (for testing)
* A wallet address to receive payments
* An [OnchainKit API key](https://onchainkit.xyz) (optional, for enhanced wallet features)

## Quick Start with the Official Example

The fastest way to build an x402-powered Mini App is using our official example:

```bash theme={null}