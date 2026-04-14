# @coinbase/create-cdp-app
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/create-cdp-app/index



This package contains the `@coinbase/create-cdp-app` CLI command, which allows developers to quickly bootstrap a React App using the CDP Web SDK.

## Quickstart

This guide will help you get started with `@coinbase/create-cdp-app`. You'll learn how to create a new CDP-enabled React application with just a few commands.

### Prerequisites

Before you begin, make sure you have one of the following package managers installed:

* [pnpm](https://pnpm.io/) (recommended)
* [npm](https://www.npmjs.com/)
* [yarn](https://yarnpkg.com/)

Gather your project ID and whitelist your app from the CDP Portal:

1. Sign in or create an account on the [CDP Portal](https://portal.cdp.coinbase.com)
2. Copy your Project ID from the dashboard
3. Go to the [Embedded Wallets CORS settings](https://portal.cdp.coinbase.com/products/embedded-wallets/cors)
4. Click add origin and whitelist `http://localhost:3000` (or wherever your app will run)

### Create Your First CDP App

You can create a new CDP app using any of these methods:

```bash theme={null}