# Demo App Tutorial
Source: https://docs.cdp.coinbase.com/embedded-wallets/demo-app-tutorial



## Overview

Build a complete React demo app from scratch to learn embedded wallets! This tutorial uses `cdp-create-app` to create a working app, then explains the key concepts and code.

## Prerequisites

* A free [CDP Portal](https://portal.cdp.coinbase.com) account and project
* [Node.js 22+](https://nodejs.org/en/download)
* A node package manager installed (i.e., `npm`, `pnpm`, or `yarn`)
* Basic familiarity with React and TypeScript
* Configured your domain in CDP Portal (see below)

<Accordion title="How to configure your domain in CDP Portal">
  **Step 1: Access CDP Portal**

  Navigate to the [Security Configuration](https://portal.cdp.coinbase.com/products/embedded-wallets/security) in CDP Portal, and click **Add domain** to include your local app.

  <Frame>
    <img alt="Add domain dialog in CDP Portal" />
  </Frame>

  **Step 2: Add your domain**

  * For local development: Use `http://localhost:3000` (or your preferred port)
  * For production: Use your actual domain (e.g., `https://yourapp.com`)

  <Frame>
    <img alt="Domain configuration with localhost" />
  </Frame>

  <Warning>
    For production apps, only add your actual production domain. Do not add `localhost` to production CDP projects as malicious apps running locally could impersonate your frontend and abuse your project credentials.
  </Warning>

  **Step 3: Save your changes**

  Click **Add domain** again to save your changes.

  <Frame>
    <img alt="Domain configuration saved in CDP Portal" />
  </Frame>

  You should see your domain listed in the CDP Portal dashboard. The allowlist will take effect immediately upon saving.
</Accordion>

<TypeScriptConfigRequirement />

## Create the demo app

<Steps>
  <Step title="Copy your Project ID">
    Navigate to [CDP Portal](https://portal.cdp.coinbase.com) and select your project from the top-left dropdown. Clicking the gear icon will take you to your project details:

    <Frame>
      <img alt="CDP Project ID in project settings" />
    </Frame>

    Copy the **Project ID** value. You will use this in the next step when configuring your demo app.
  </Step>

  <Step title="Create a new demo app">
    Use the latest version of `create-cdp-app` to create a new demo app. Replace `<your-project-id>` with your actual project ID from the previous step:

    <CodeGroup>
      ```bash npm theme={null}
      npm create @coinbase/cdp-app@latest cdp-app-react -- --template react --project-id <your-project-id>
      ```

      ```bash pnpm theme={null}
      pnpm create @coinbase/cdp-app@latest cdp-app-react -- --template react --project-id <your-project-id>
      ```

      ```bash yarn theme={null}
      yarn create @coinbase/cdp-app@latest cdp-app-react -- --template react --project-id <your-project-id>
      ```
    </CodeGroup>
  </Step>

  <Step title="Select account type">
    You will be prompted to choose between EVM EOA (Regular Accounts), EVM Smart Accounts, or Solana Accounts:

    ```console theme={null}
    Account Type:
    ❯   EVM EOA (Regular Accounts)
        EVM Smart Accounts
        Solana Accounts
    ```
  </Step>

  <Step title="Confirm domain whitelist">
    You will be prompted to confirm the localhost domain (which you should have already configured in the setup above):

    ```console theme={null}
    ✔ Confirm you have whitelisted 'http://localhost:3000' by typing 'y' … y
    ```
  </Step>

  <Step title="Run your app">
    Navigate to your project directory, install dependencies, and start the development server:

    <CodeGroup>
      ```bash npm theme={null}
      cd cdp-app-react
      npm install
      npm run dev
      ```

      ```bash pnpm theme={null}
      cd cdp-app-react
      pnpm install
      pnpm dev
      ```

      ```bash yarn theme={null}
      cd cdp-app-react
      yarn install
      yarn dev
      ```
    </CodeGroup>
  </Step>
</Steps>

On successful startup, you should see similar to the following:

```console theme={null}
  VITE v7.0.5  ready in 268 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

## Demo your new wallet

Now that your embedded wallet is configured and your app is running, let's try it out.

<Steps>
  <Step title="Sign in">
    Head to [http://localhost:3000](http://localhost:3000) and click the **Sign In** button.

    <Frame>
      <img alt="CDP React Demo Sign In" />
    </Frame>
  </Step>

  <Step title="Enter your email">
    <Frame>
      <img alt="CDP React Demo Email" />
    </Frame>
  </Step>

  <Step title="Verify">
    Enter the verification code sent to your e-mail.

    <Frame>
      <img alt="CDP React Demo Verify" />
    </Frame>
  </Step>

  <Step title="View your new wallet">
    Congrats! Your new embedded wallet has been created, authenticated, and is ready to use on the [Base Sepolia](https://sepolia.basescan.org/) network if you selected an EVM account type, or [Solana Devnet](https://explorer.solana.com?cluster=devnet) if you selected Solana Accounts.

    <details>
      <summary><strong>What is Base?</strong></summary>

      **Base** is a fast, low-cost blockchain built by Coinbase. **Base Sepolia** is its test network where you can experiment with fake money (testnet ETH) before deploying to production.
    </details>

    From the demo app, you can copy-and-paste your wallet address from the top-right corner. You can also monitor your wallet balance and (eventually -- keep reading!) send transactions. You should see similar to the following:

    <Frame>
      <img alt="CDP React Demo Transaction" />
    </Frame>

    Find record of your new wallet on Base Sepolia explorer using the URL: `https://sepolia.basescan.org/address/YOUR-WALLET-ADDRESS`.
  </Step>

  <Step title="Fund your wallet with testnet ETH or SOL">
    Before you can send transactions, you'll need to fund your wallet with the network gas token. Follow the link to request testnet funds from a Base or Solana [Faucet](/faucets/introduction/welcome).

    <details>
      <summary><strong>What is a transaction?</strong></summary>

      A blockchain transaction transfers cryptocurrency between wallets. Unlike bank transfers, they're:

      * **Public**: Visible on the blockchain
      * **Permanent**: Cannot be reversed
      * **Fast**: Usually complete in seconds
      * **Fee-based**: Require "gas" fees to process
    </details>

    <details>
      <summary><strong>What are testnet funds?</strong></summary>

      **Testnet funds** are fake cryptocurrency for testing. You get them free from a **faucet** (a service that "drips" test ETH to developers). Testnet funds are "play money" you can use for experimenting, without risking real money.
    </details>

    <Frame>
      <img alt="CDP React Demo Fund Wallet" />
    </Frame>
  </Step>

  <Step title="Send your first transaction">
    Now that your wallet has testnet ETH, you can send your first transaction!
    For EVM accounts, the demo app allows you to send 0.000001 ETH to yourself as a test.
    For Solana accounts, it will similarly send 0.000000001 SOL.

    Click **Send Transaction** to initiate the transfer. Once complete, you'll see a transaction hash that you can look up on the blockchain explorer.

    <Frame>
      <img alt="CDP React Demo Transaction" />
    </Frame>

    🎉 You've successfully created an embedded wallet and sent your first transaction! Try adding some [React Hooks](/embedded-wallets/react-hooks) or additional [components](/embedded-wallets/react-components) to expand your app.
  </Step>
</Steps>

## How it works

Want to customize your app or understand how CDP makes wallets so simple? Let's look at the key components that power your new embedded wallet.

### File structure

The demo app is built with React and [Vite](https://vite.dev/), organized into these main files:

```
src/
├── App.tsx              # Main app component with authentication state
├── SignInScreen.tsx     # Sign-in UI component
├── SignedInScreen.tsx   # Post-authentication UI with balance tracking
├── Header.tsx           # Header with wallet address and auth button
├── Transaction.tsx      # Transaction sending component
├── UserBalance.tsx      # Balance display component
├── Loading.tsx          # Loading state component
├── Icons.tsx            # Icon components
├── config.ts            # CDP configuration
├── theme.ts             # Custom theme configuration
├── main.tsx             # Entry point
└── index.css            # Styles
```

<Tip>
  You can explore the package for this demo in more detail at [npmjs.com](https://www.npmjs.com/package/@coinbase/create-cdp-app?activeTab=code).
</Tip>

### Entry point + provider setup

`src/main.tsx` demonstrates how to wrap your app with the `CDPReactProvider` to enable CDP functionality throughout the component tree.

```tsx src/main.tsx theme={null}
import { type Config, CDPReactProvider } from "@coinbase/cdp-react";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App.tsx";
import { CDP_CONFIG } from "./config.ts";
import { theme } from "./theme.ts";
import "./index.css";

const config: Config = {
  ...CDP_CONFIG,
  ethereum: {
    createOnLogin: "eoa",
  },
  appName: "Your App Name", // Your app's display name shown in the wallet UI
  appLogoUrl: "your-app-logo-url", // URL to your app's logo displayed during authentication
  authMethods: ["email", "sms"],
};

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <CDPReactProvider config={config} theme={theme}>
      <App />
    </CDPReactProvider>
  </StrictMode>,
);
```

The `CDP_CONFIG` contains your **Project ID** from setup, stored securely in an environment variable (`VITE_CDP_PROJECT_ID`).
By default the app creates an EVM EOA account for the user on sign in.
To create a Smart Account, set `ethereum.createOnLogin` to `smart` in the config.

<Note>
  You may create both an EVM (EOA or Smart) account and a Solana account on login.
  To create a Solana account, set `solana.createOnLogin` to `true` in the config.

  For the following examples, we will be assuming an EVM EOA account setup.
</Note>

### Auth state management

`src/App.tsx` demonstrates how CDP simplifies wallet state management with two simple hooks:

```tsx src/App.tsx theme={null}
import { useIsInitialized, useIsSignedIn } from "@coinbase/cdp-hooks";

import Loading from "./Loading";
import SignedInScreen from "./SignedInScreen";
import SignInScreen from "./SignInScreen";

function App() {
  const { isInitialized } = useIsInitialized();
  const { isSignedIn } = useIsSignedIn();

  return (
    <div className="app flex-col-container flex-grow">
      {!isInitialized && <Loading />}
      {isInitialized && (
        <>
          {!isSignedIn && <SignInScreen />}
          {isSignedIn && <SignedInScreen />}
        </>
      )}
    </div>
  );
}

export default App;
```

CDP provides these powerful hooks:

* `useIsInitialized()`: Know when the SDK is ready (no manual provider checks!)
* `useIsSignedIn()`: Instant auth status (no complex wallet connection state)

Unlike traditional Web3 apps that manage wallet providers, connection states, account changes, and network switches, CDP handles everything behind the scenes. Your app just checks if the user is signed in.

### Sign-in interface

`src/SignInScreen.tsx` showcases how to provide the Sign in experience to your users.

```tsx src/SignInScreen.tsx theme={null}
import { AuthButton } from "@coinbase/cdp-react/components/AuthButton";

function SignInScreen() {
  return (
    <main className="card card--login">
      <h1 className="sr-only">Sign in</h1>
      <p className="card-title">Welcome!</p>
      <p>Please sign in to continue.</p>
      <AuthButton />
    </main>
  );
}

export default SignInScreen;
```

The `AuthButton` component handles:

* **Email authentication**: No seed phrases to manage - users maintain full control
* **Wallet creation**: Automatically creates a self-custodial wallet on first sign-in
* **Session management**: Handles tokens and persistence
* **UI/UX**: Professional auth flow with email verification

### The authenticated experience

`src/SignedInScreen.tsx` shows how to manage the authenticated session of a user.

Two important hooks to highlight here:

* `useEvmAddress()`: Fetch the user's wallet address
* `useIsSignedIn()`: Returns true if the user is signed in

For balance tracking, we query the blockchain using the user's wallet address:

```tsx src/SignedInScreen.tsx theme={null}
  const getBalance = useCallback(async () => {
    if (!evmAddress) return;
    
    // Query the blockchain for the user's evm address
    const balance = await client.getBalance({
      address: evmAddress,
    });
    setBalance(balance);
  }, [evmAddress]);

  // Refresh balance on mount and every 500ms
  useEffect(() => {
    getBalance();
    const interval = setInterval(getBalance, 500);
    return () => clearInterval(interval);
  }, [getBalance]);
```

Finally, we compose the authenticated UI to return the user's balance:

```tsx src/SignedInScreen.tsx theme={null}
  return (
    <>
      <Header />
      <main className="main flex-col-container flex-grow">
        <div className="main-inner flex-col-container">
          <div className="card card--user-balance">
            <UserBalance balance={formattedBalance} />
          </div>
          <div className="card card--transaction">
            {isSignedIn && evmAddress && (
              <Transaction 
                balance={formattedBalance} 
                onSuccess={getBalance}
              />
            )}
          </div>
        </div>
      </main>
    </>
  );
}
```

### Sending transactions

`src/Transaction.tsx` demonstrates how to send ETH using CDP's transaction hooks.

Key CDP hooks to highlight here:

* `useSendEvmTransaction()`: Sends transactions from the user's address
* `useEvmAddress()`: Gets the current user's address

We create the transaction handler using CDP's `sendEvmTransaction`:

```tsx src/Transaction.tsx theme={null}
  const handleSendTransaction = useCallback(
    async (e: MouseEvent<HTMLButtonElement>) => {
      if (!evmAddress) return;

      e.preventDefault();
      setIsPending(true);

      const { transactionHash } = await sendEvmTransaction({
        transaction: {
          to: evmAddress,              // Send to yourself for testing
          value: 1000000000000n,       // 0.000001 ETH in wei
          gas: 21000n,                 // Standard ETH transfer gas limit
          chainId: 84532,              // Base Sepolia testnet
          type: "eip1559",             // Modern gas fee model
        },
        evmAccount: evmAddress,        // Your self-custodial wallet address
        network: "base-sepolia",       // Target network
      });

      setTransactionHash(transactionHash);
      setIsPending(false);
      onSuccess?.();
    },
    [evmAddress, sendEvmTransaction, onSuccess],
  );
```

Finally, the UI renders different content based on the transaction state:

```tsx src/Transaction.tsx theme={null}
  return (
    <>
      {transactionHash ? (
        // Success state
        <>
          <h2>Transaction sent</h2>
          <a href={`https://sepolia.basescan.org/tx/${transactionHash}`}>
            {transactionHash.slice(0, 6)}...{transactionHash.slice(-4)}
          </a>
          <Button onClick={() => setTransactionHash(null)}>
            Send another transaction
          </Button>
        </>
      ) : (
        // Pre-transaction state (ready to send or needs funds)
        <>
          {hasBalance ? (
            <Button onClick={handleSendTransaction} isPending={isPending}>
              Send Transaction
            </Button>
          ) : (
            <p>Get testnet ETH from the faucet first!</p>
          )}
        </>
      )}
    </>
  );
```

The component intelligently handles different states:

* Loading skeletons while fetching balance
* Empty wallet state with faucet link
* Ready state with send button
* Success state with transaction hash and option to send another

### Wallet management header

`src/Header.tsx` provides a clean interface for users to view their wallet address and manage their session.

```tsx src/Header.tsx theme={null}
function Header() {
  const evmAddress = useEvmAddress();  // Get the user's address
  const [isCopied, setIsCopied] = useState(false);

  const copyAddress = async () => {
    await navigator.clipboard.writeText(evmAddress);
    setIsCopied(true);
    // Reset after 2 seconds
    setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <header>
      <h1>CDP React StarterKit</h1>
      <div className="user-info">
        {/* Copy wallet address button */}
        <button onClick={copyAddress}>
          {isCopied ? <IconCheck /> : <IconCopy />}
          <span>{evmAddress.slice(0, 6)}...{evmAddress.slice(-4)}</span>
        </button>
        
        {/* Sign out button */}
        <AuthButton />
      </div>
    </header>
  );
}
```

Key features:

* **Wallet display**: Shows truncated address (e.g., `0x1234...5678`)
* **Copy to clipboard**: One-click copying with visual feedback
* **Session management**: Sign out via CDP's `AuthButton`

### Balance display

`src/UserBalance.tsx` displays the user's ETH balance with a helpful faucet link.

```tsx src/UserBalance.tsx theme={null}
function UserBalance({ balance }: { balance?: string }) {
  return (
    <>
      <h2 className="card-title">Available balance</h2>
      <p className="user-balance">
        {balance === undefined && <LoadingSkeleton />}
        {balance !== undefined && (
          <span className="flex-row-container">
            <img src="/eth.svg" alt="" className="balance-icon" />
            <span>{balance}</span>
          </span>
        )}
      </p>
      <p>
        Get testnet ETH from{" "}
        <a href="https://portal.cdp.coinbase.com/products/faucet">
          Base Sepolia Faucet
        </a>
      </p>
    </>
  );
}
```

Key features:

* Shows ETH balance with an icon
* Loading skeleton while fetching balance
* Direct link to the faucet for getting testnet funds

### Theme customization

The demo app provides extensive theming capabilities through CSS variables and the CDP theme system, allowing you to fully customize the look and feel to match your brand.

```tsx src/theme.ts theme={null}
export const theme: Partial<Theme> = {
  "colors-bg-default": "var(--cdp-example-card-bg-color)",
  "colors-bg-overlay": "var(--cdp-example-bg-overlay-color)",
  "colors-bg-skeleton": "var(--cdp-example-bg-skeleton-color)",
  "colors-bg-primary": "var(--cdp-example-accent-color)",
  "colors-bg-secondary": "var(--cdp-example-bg-low-contrast-color)",
  "colors-fg-default": "var(--cdp-example-text-color)",
  "colors-fg-muted": "var(--cdp-example-text-secondary-color)",
  "colors-fg-primary": "var(--cdp-example-accent-color)",
  "colors-fg-onPrimary": "var(--cdp-example-accent-foreground-color)",
  "colors-fg-onSecondary": "var(--cdp-example-text-color)",
  "colors-line-default": "var(--cdp-example-card-border-color)",
  "colors-line-heavy": "var(--cdp-example-text-secondary-color)",
  "colors-line-primary": "var(--cdp-example-accent-color)",
  "font-family-sans": "var(--cdp-example-font-family)",
  "font-size-base": "var(--cdp-example-base-font-size)",
  // ... maps to CSS variables defined in index.css
};
```

The app includes:

* **Dark mode support**: Enables light and dark themes
* **Customizable colors**: Primary accent, backgrounds, text, borders, and more
* **Typography control**: Font family and base font size
* **Responsive breakpoints**: Different styles for mobile, tablet, and desktop
* **Component theming**: Style CDP components like buttons, inputs, and modals

All theme values are defined as CSS variables in `index.css`, making it easy to rebrand the entire app by updating a few color values.

For more information on theme customization, see the [theme customization documentation](/embedded-wallets/react-components#3-customize-theme-optional).

## What to read next

<CardGroup>
  <Card title="Quickstart" icon="rocket" href="/embedded-wallets/quickstart">
    Quick integration guide for existing React apps
  </Card>

  <Card title="React Hooks" icon="code" href="/embedded-wallets/react-hooks">
    Learn about available hooks like useSignInWithEmail, useEvmAddress, useSendSolanaTransaction, and more
  </Card>

  <Card title="React Components" icon="puzzle-piece" href="/embedded-wallets/react-components">
    Explore pre-built components for authentication, wallet management, and transactions
  </Card>

  <Card title="Next.js Integration" icon="arrow-right" href="/embedded-wallets/nextjs">
    Build with Next.js using "use client" requirements
  </Card>
</CardGroup>

