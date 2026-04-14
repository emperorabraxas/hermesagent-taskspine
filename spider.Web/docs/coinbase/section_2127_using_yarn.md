# Using yarn
yarn create @coinbase/cdp-app@latest
```

The CLI will guide you through the setup process:

1. Enter your project name (defaults to "cdp-app")
2. Select a template (React, Next.js, or React Native)
3. Enter your CDP Project ID
4. Select account type (EVM EOA, EVM Smart Accounts, or Solana)
5. Configure Onramp (Next.js only)
6. Confirm you have whitelisted your app domain on the CDP Portal
7. Confirm directory overwrite if needed

## Available Templates

Currently, `create-cdp-app` offers the following templates:

* **React** (`react`): A React application template that includes:
  * Vite for fast development and building
  * TypeScript for type safety
  * CDP React components for authentication
  * Example transaction components
  * Base Sepolia integration
* **Next.js** (`nextjs`): A Next.js application template that includes:
  * Next.js 15 App Router
  * CDP React components for authentication and wallet management
  * Example transaction components for Base Sepolia
  * Built-in TypeScript support
  * ESLint with Next.js configuration
  * Viem for type-safe Ethereum interactions
* **React Native** (`react-native`): A React Native with Expo template that includes:
  * Expo SDK for cross-platform mobile development
  * CDP React Native components for authentication
  * Example transaction components
  * TypeScript support
  * Support for both iOS and Android

## Command-Line Arguments

You can also pass command-line arguments to pre-configure the setup process.

| Argument                | Description                                                                                                                                                                                                                                                                     |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `<directory>`           | Optional. The name of the directory to create the project in. Defaults to `cdp-app`.                                                                                                                                                                                            |
| `--template <name>`     | Specifies the project template to use. Options: `react`, `nextjs`, `react-native`.                                                                                                                                                                                              |
| `--project-id <id>`     | Your CDP Project ID from the portal.                                                                                                                                                                                                                                            |
| `--account-type <type>` | Specifies the account type to configure. Options: `evm-eoa` (default), `evm-smart`, `solana`.                                                                                                                                                                                   |
| `--onramp`              | Enables Coinbase Onramp. <br />**Note:** This is only compatible with the `nextjs` template. If no template is specified, `nextjs` will be used automatically. If an incompatible template (e.g., `react`) is specified, this flag will be ignored and Onramp will be disabled. |
| `--no-onramp`           | Disables Coinbase Onramp.                                                                                                                                                                                                                                                       |

### Examples

```bash theme={null}