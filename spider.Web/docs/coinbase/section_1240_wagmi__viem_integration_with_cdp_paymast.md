# Wagmi + Viem Integration with CDP Paymaster
Source: https://docs.cdp.coinbase.com/paymaster/guides/wagmi-viem-integration



This guide covers how to integrate CDP Paymaster for gasless transactions in a Wagmi project using the Base Account SDK. You'll configure Wagmi with the `baseAccount` connector and use Wagmi's hooks to execute sponsored transactions.

<Info>
  This guide uses the [Base Account SDK](https://docs.base.org/base-account) which provides a streamlined connector for Wagmi. For CDP Embedded Wallets integration, see the [Quickstart](/paymaster/introduction/quickstart).
</Info>

## Prerequisites

* A [CDP account](https://portal.cdp.coinbase.com) with Paymaster enabled
* Node.js 22+ and a package manager (npm, pnpm, yarn, or bun)
* Basic familiarity with React and Wagmi

## Step 1: Set Up CDP Paymaster

1. [Sign in](https://portal.cdp.coinbase.com) to your CDP account
2. Navigate to [**Onchain Tools > Paymaster**](https://portal.cdp.coinbase.com/products/bundler-and-paymaster)
3. Select your network (**Base** or **Base Sepolia**) in the top right
4. Copy your **Paymaster & Bundler endpoint** URL
5. Under **Configuration**, add any contracts you want to sponsor to the allowlist

<Warning>
  **Security:** Your Paymaster endpoint should not be exposed in client-side code. For production, use a [proxy service](/paymaster/guides/paymaster-proxy) to protect your API key.
</Warning>

Add the endpoint to your environment:

```bash title=".env" theme={null}
CDP_PAYMASTER_URL=https://api.developer.coinbase.com/rpc/v1/base-sepolia/YOUR_API_KEY
```

## Step 2: Install Dependencies

### New Wagmi Project

Create a new Wagmi project and override the Base Account SDK version:

```bash theme={null}