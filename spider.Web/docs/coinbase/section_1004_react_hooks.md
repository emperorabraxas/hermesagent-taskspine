# React Hooks
Source: https://docs.cdp.coinbase.com/embedded-wallets/react-hooks



<Tags />

## Overview

Coinbase Developer Platform (CDP) provides React hooks for conveniently accessing the CDP Embedded Wallet SDK functionality on both EVM and Solana networks.

Built on top of `@coinbase/cdp-core`, these hooks offer a React-friendly interface for authentication and embedded wallet operations.

<Tip>
  For a complete list of available hooks with comprehensive method signatures, types, and examples, see the [CDP Web SDK reference](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks).
</Tip>

## Prerequisites

The fastest way to get started is to complete the [Quickstart](/embedded-wallets/quickstart). If you already have your own app, you should complete the prerequisites below before proceeding. You will need:

1. A [CDP Portal](https://portal.cdp.coinbase.com) account and CDP project
2. [Node.js 22+](https://nodejs.org/en/download) installed
3. Your local app domain [configured](/embedded-wallets/domains) in CDP Portal
4. A package manager of your choice, with `cdp-hooks` installed:

<CodeGroup>
  ```bash npm theme={null}
  npm install @coinbase/cdp-core @coinbase/cdp-hooks
  ```

  ```bash pnpm theme={null}
  pnpm add @coinbase/cdp-core @coinbase/cdp-hooks
  ```

  ```bash yarn theme={null}
  yarn add @coinbase/cdp-core @coinbase/cdp-hooks
  ```
</CodeGroup>

## 1. Setup hooks provider

If you're not using the demo app from the Quickstart, you'll need to manually set up the `CDPHooksProvider` in your application:

<Warning>
  **Using Next.js?** Check out our [Next.js integration guide](/embedded-wallets/nextjs) for `"use client"` requirements and common gotchas.
</Warning>

```tsx theme={null}
import { CDPHooksProvider } from "@coinbase/cdp-hooks";

function App() {
  return (
    <CDPHooksProvider
      config={{
        projectId: "your-project-id",
        basePath: "https://api.cdp.coinbase.com", // CDP API url
        useMock: false, // Use live APIs or use mock data for testing
        debugging: false, // Log API requests and responses
      }}
    >
      <YourApp />
    </CDPHooksProvider>
  );
}
```

Config options:

* `projectId` (required)
* `ethereum.createOnLogin` = `"eoa" | "smart"` (optional)
* `solana.createOnLogin` = `boolean` (optional)
* `basePath` (optional API base URL)
* `useMock` (optional mock mode for local testing)
* `debugging` (optional verbose API logging)

Check out the [Smart Accounts guide](/embedded-wallets/smart-accounts) for more information about EVM smart accounts.

## 2. Ensure SDK initialization

Always ensure the SDK is initialized before authenticating a user or performing wallet operations:

```tsx theme={null}
import { useIsInitialized } from "@coinbase/cdp-hooks";

function App() {
  const { isInitialized } = useIsInitialized();

  if (!isInitialized) {
    return <div>Loading...</div>;
  }

  return <Page />;
}
```

## Hook examples

Now let's explore how to use CDP hooks to build wallet functionality into your React application.

### User sign-in

Our authentication uses a two-step flow:

1. Submit user email to initiate the authentication flow, which will send the user a One-Time-Password (OTP) and return a `flowId`
2. Submit the six-digit OTP and `flowId`, after which the user will be authenticated, returning a User object

```tsx theme={null}
import { useSignInWithEmail, useVerifyEmailOTP } from "@coinbase/cdp-hooks";

function SignIn() {
  const { signInWithEmail } = useSignInWithEmail();
  const { verifyEmailOTP } = useVerifyEmailOTP();

  const handleSignIn = async (email: string) => {
    try {
      // Start sign in flow
      const { flowId } = await signInWithEmail({ email });

      // Get OTP from user input...
      const otp = "123456";

      // Complete sign in
      const { user, isNewUser } = await verifyEmailOTP({
        flowId,
        otp
      });

      console.log("Signed in user:", user);
      console.log("EVM address:", user.evmAccounts[0]);
      console.log("Solana address:", user.solanaAccounts[0]);
    } catch (error) {
      console.error("Sign in failed:", error);
    }
  };

  return <button onClick={() => handleSignIn("user@example.com")}>Sign In</button>;
}
```

#### OAuth sign-in

Sign in with social providers using the OAuth flow. Note that the page from which the `signInWithOAuth` call occurs will be redirected back to after the user authenticates with their provider. The user will be automatically logged-in when `@coinbase/cdp-core` re-initializes.

<CodeGroup>
  ```tsx Google OAuth theme={null}
  import { useSignInWithOAuth } from "@coinbase/cdp-hooks";

  function SignIn() {
    const { signInWithOAuth } = useSignInWithOAuth();

    const handleGoogleSignIn = () => {
      // User will be redirected to Google to complete their login
      // After login, they will be redirected back to your app, and the login
      // process will be completed automatically by the SDK
      void signInWithOAuth("google");
    };

    return <button onClick={handleGoogleSignIn}>Sign In with Google</button>;
  }
  ```

  ```tsx Apple OAuth theme={null}
  import { useSignInWithOAuth } from "@coinbase/cdp-hooks";

  function SignIn() {
    const { signInWithOAuth } = useSignInWithOAuth();

    const handleAppleSignIn = () => {
      // User will be redirected to Apple to complete their login
      // After login, they will be redirected back to your app, and the login
      // process will be completed automatically by the SDK
      void signInWithOAuth("apple");
    };

    return <button onClick={handleAppleSignIn}>Sign In with Apple</button>;
  }
  ```

  ```tsx Telegram OAuth theme={null}
  import { useSignInWithOAuth } from "@coinbase/cdp-hooks";

  function SignIn() {
    const { signInWithOAuth } = useSignInWithOAuth();

    const handleTelegramSignIn = () => {
      // User will be redirected to Telegram to complete their login
      // After login, they will be redirected back to your app, and the login
      // process will be completed automatically by the SDK
      void signInWithOAuth("telegram");
    };

    return <button onClick={handleTelegramSignIn}>Sign In with Telegram</button>;
  }
  ```
</CodeGroup>

### View user profile

Display user information and wallet addresses using CDP hooks:

<Tabs>
  <Tab title="evmProfile.tsx">
    ```tsx theme={null}
    import { useCurrentUser, useEvmAddress } from "@coinbase/cdp-hooks";

    function Profile() {
      const { currentUser } = useCurrentUser();
      const { evmAddress } = useEvmAddress();

      if (!currentUser) {
        return <div>Please sign in</div>;
      }

      return (
        <div>
          <h2>Profile</h2>
          <p>User ID: {currentUser.userId}</p>
          <p>EVM Address: {evmAddress}</p>
          <p>All EVM Accounts: {currentUser.evmAccounts.join(", ")}</p>
          {currentUser.evmSmartAccounts?.[0] && (
            <p>Smart Account: {currentUser.evmSmartAccounts[0]}</p>
          )}
        </div>
      );
    }
    ```
  </Tab>

  <Tab title="solanaProfile.tsx">
    ```tsx theme={null}
    import { useCurrentUser, useSolanaAddress } from "@coinbase/cdp-hooks";

    function Profile() {
      const { currentUser } = useCurrentUser();
      const { solanaAddress } = useSolanaAddress();

      if (!currentUser) {
        return <div>Please sign in</div>;
      }

      return (
        <div>
          <h2>Profile</h2>
          <p>User ID: {currentUser.userId}</p>
          <p>Solana Address: {solanaAddress}</p>
          <p>All Solana Accounts: {currentUser.solanaAccounts.join(", ")}</p>
        </div>
      );
    }
    ```
  </Tab>
</Tabs>

### Send a transaction

We support signing and sending a blockchain transaction in a single action on the networks listed below.

##### EVM networks:

* Base
* Base Sepolia
* Ethereum
* Ethereum Sepolia
* Arbitrum
* Avalanche
* Optimism
* Polygon

<Tip>
  **Working with Solana?** See [Solana Sending Transactions](/embedded-wallets/solana-features/sending-transactions) for Solana transaction examples.
</Tip>

```tsx evmTransaction.tsx theme={null}
import { useSendEvmTransaction, useEvmAddress } from "@coinbase/cdp-hooks";

function SendTransaction() {
  const { sendEvmTransaction } = useSendEvmTransaction();
  const { evmAddress } = useEvmAddress();

  const handleSend = async () => {
    if (!evmAddress) return;

    try {
      const result = await sendEvmTransaction({
        transaction: {
          to: evmAddress,              // Send to yourself for testing
          value: 1000000000000n,       // 0.000001 ETH in wei
          gas: 21000n,                 // Standard ETH transfer gas limit
          chainId: 84532,              // Base Sepolia
          type: "eip1559",             // Modern gas fee model
        },
        evmAccount: evmAddress,        // Your CDP wallet address
        network: "base-sepolia",       // Target network
      });

      console.log("Transaction hash:", result.transactionHash);
    } catch (error) {
      console.error("Transaction failed:", error);
    }
  };

  return <button onClick={handleSend}>Send Transaction</button>;
}
```

<Note>
  The `useSendEvmTransaction` hook also returns a `data` state with statuses `idle | pending | success | error` that reflects the most recent transaction.
</Note>

### Sign and broadcast (non-supported EVM networks)

For networks other than those supported by the Send Transaction API, you can sign a transaction with the wallet and broadcast it yourself. This example uses the public client from `viem` to broadcast the transaction.

Common use cases include [Tempo](/embedded-wallets/evm-features/tempo) (a stablecoin payments blockchain) and other EVM-compatible chains not listed above.

```tsx theme={null}
import { useSignEvmTransaction, useEvmAddress } from "@coinbase/cdp-hooks";
import { http, createPublicClient } from "viem";
import { tron } from "viem/chains";

function NonBaseTransaction() {
  const { signEvmTransaction } = useSignEvmTransaction();
  const { evmAddress } = useEvmAddress();

  const handleSend = async () => {
    if (!evmAddress) return;

    try {
      // Sign the transaction
      const { signedTransaction } = await signEvmTransaction({
        evmAccount: evmAddress,
        transaction: {
          to: evmAddress,              // Send to yourself for testing
          value: 1000000000000n,       // 0.000001 ETH in wei
          gas: 21000n,                 // Standard ETH transfer gas limit
          chainId: 728126428,          // Tron
          type: "eip1559",             // Modern gas fee model
        }
      });

      // Broadcast using a different client
      const client = createPublicClient({
        chain: tron,
        transport: http()
      });

      const hash = await client.sendRawTransaction({
        serializedTransaction: signedTransaction
      });

      console.log("Transaction hash:", hash);
    } catch (error) {
      console.error("Transaction failed:", error);
    }
  };

  return <button onClick={handleSend}>Send Transaction</button>;
}
```

### Sign messages and typed data

You can sign EVM messages, hashes, and typed data to generate signatures for various on-chain applications:

<Tip>
  **Working with Solana?** See [Solana Signing](/embedded-wallets/solana-features/signing) for Solana message and transaction signing examples.
</Tip>

```tsx evmSigning.tsx theme={null}
import { useSignEvmMessage, useSignEvmTypedData, useSignEvmHash, useEvmAddress } from "@coinbase/cdp-hooks";

function SignData() {
  const { signEvmMessage } = useSignEvmMessage();
  const { signEvmTypedData } = useSignEvmTypedData();
  const { signEvmHash } = useSignEvmHash();
  const { evmAddress } = useEvmAddress();

  const handleSignMessage = async () => {
    if (!evmAddress) return;

    const result = await signEvmMessage({
      evmAccount: evmAddress,
      message: "Hello World"
    });

    console.log("Message signature:", result.signature);
  };

  const handleSignTypedData = async () => {
    if (!evmAddress) return;

    const result = await signEvmTypedData({
      evmAccount: evmAddress,
      typedData: {
        domain: {
          name: "Example DApp",
          version: "1",
          chainId: 84532,
        },
        types: {
          Person: [
            { name: "name", type: "string" },
            { name: "wallet", type: "address" }
          ]
        },
        primaryType: "Person",
        message: {
          name: "Bob",
          wallet: evmAddress
        }
      }
    });

    console.log("Typed data signature:", result.signature);
  };

  const handleSignHash = async () => {
    if (!evmAddress) return;

    const result = await signEvmHash({
      evmAccount: evmAddress,
      hash: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    });

    console.log("Hash signature:", result.signature);
  };

  return (
    <div>
      <button onClick={handleSignMessage}>Sign Message</button>
      <button onClick={handleSignTypedData}>Sign Typed Data</button>
      <button onClick={handleSignHash}>Sign Hash</button>
    </div>
  );
}
```

### Export private keys

<Warning>
  Private key export is a high-risk security operation. See our comprehensive [Security & Export](/embedded-wallets/security-export) guide for proper implementation, security considerations, and best practices.
</Warning>

The `useExportEvmAccount` and `useExportSolanaAccount` hooks allows users to export their respective private keys for wallet migration or other purposes. For detailed implementation examples and security guidance, see the [Security & Export](/embedded-wallets/security-export#implementation) documentation.

### Send a user operation (Smart Accounts)

Send user operations from Smart Accounts with support for multiple calls and paymaster sponsorship. The hook returns a method to execute the user operation and forwards `status`, `data`, and `error` from its internal tracking.

```tsx theme={null}
import { useSendUserOperation, useCurrentUser } from "@coinbase/cdp-hooks";

function SendUserOperation() {
  const { sendUserOperation } = useSendUserOperation();
  const { currentUser } = useCurrentUser();

  const handleSendUserOperation = async () => {
    const smartAccount = currentUser?.evmSmartAccounts?.[0];
    if (!smartAccount) return;

    try {
      // This will automatically start tracking the user operation status
      const result = await sendUserOperation({
        evmSmartAccount: smartAccount,
        network: "base-sepolia",
        calls: [{
          to: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
          value: 1000000000000000000n,
          data: "0x",
        }],
      });

      console.log("User Operation Hash:", result.userOperationHash);
    } catch (error) {
      console.error("Failed to send user operation:", error);
    }
  };

  return <button onClick={handleSendUserOperation}>Send User Operation</button>;
}
```

The hook returns the `sendUserOperation` method, which you call with the transaction parameters that you want to send. The hook also returns `status`, `data`, and `error` values which you can use to track the status of the user operation. For more information, see the [Smart Accounts guide](/embedded-wallets/smart-accounts#send-a-user-operation).

## What to read next

* [**CDP Web SDK Documentation**](/sdks/cdp-sdks-v2/frontend): Comprehensive API reference for the CDP Web SDK
* [**Embedded Wallet - React Components**](/embedded-wallets/react-components): Pre-built UI components that work seamlessly with these hooks
* [**Embedded Wallet - Wagmi Integration**](/embedded-wallets/wagmi): Use CDP wallets with the popular wagmi library
* [**Embedded Wallet - Next.js**](/embedded-wallets/nextjs): Special considerations for Next.js applications
* [**Embedded Wallet - Smart Accounts**](/embedded-wallets/smart-accounts): Dedicated guide for ERC-4337 features and paymasters (spend permissions coming soon)
* [**Tempo Integration**](/embedded-wallets/evm-features/tempo): Sign and broadcast transactions on the Tempo stablecoin payments blockchain

