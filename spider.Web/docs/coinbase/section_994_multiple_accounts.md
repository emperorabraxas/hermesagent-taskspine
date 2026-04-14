# Multiple Accounts
Source: https://docs.cdp.coinbase.com/embedded-wallets/multiple-accounts



<Tags />

## Overview

Users can create multiple blockchain accounts of each type within their Embedded Wallet. This enables organizing funds across different purposes, separating assets, and managing complex workflows without requiring separate wallet authentications.

Key capabilities:

* **Up to 10 EVM EOA accounts** per user
* **Up to 10 Solana accounts** per user
* **Up to 10 EVM Smart Accounts** per user (each requires a unique EOA owner)
* **Account Metadata**: Each account includes creation timestamp and ownership information
* **Flexible creation**: Create accounts on-demand based on your application's needs

<Note>
  When `createOnLogin` is configured in your provider settings, only one account of the specified type is created automatically. Additional accounts must be created manually using the methods described below.
</Note>

## Prerequisites

* A CDP Portal account and project
* Node.js 22+ and a package manager (npm, pnpm, or yarn)
* `@coinbase/cdp-core` and `@coinbase/cdp-hooks` installed
* User must be authenticated

## Account types

### EVM EOA Accounts

Externally Owned Accounts (EOAs) are standard Ethereum accounts controlled by private keys. Users can create up to 10 EOA accounts.

### Solana Accounts

Native Solana accounts for interacting with the Solana blockchain. Users can create up to 10 Solana accounts.

### EVM Smart Accounts

Smart Accounts (ERC-4337) are programmable wallets with advanced features like batch transactions and gas sponsorship. Each Smart Account requires a unique EOA owner, and users can create up to 10 Smart Accounts (one per EOA account).

## Creating additional accounts

### Using React Hooks

React Hooks provide the most convenient way to create accounts in React applications:

<CodeGroup>
  ```tsx EVM EOA Account theme={null}
  import { useCreateEvmEoaAccount, useCurrentUser } from "@coinbase/cdp-hooks";

  function CreateEoaAccount() {
    const { createEvmEoaAccount } = useCreateEvmEoaAccount();
    const { currentUser } = useCurrentUser();

    const handleCreate = async () => {
      try {
        const account = await createEvmEoaAccount();
        console.log("New EOA created:", account.address);
        console.log("Created at:", new Date(account.createdAt).toLocaleDateString());
      } catch (error) {
        console.error("Failed to create account:", error);
      }
    };

    return (
      <div>
        <h3>Your EVM Accounts ({currentUser?.evmAccountObjects?.length || 0}/10)</h3>
        <button onClick={handleCreate}>
          Create New EOA Account
        </button>
      </div>
    );
  }
  ```

  ```tsx EVM Smart Account theme={null}
  import { useCreateEvmSmartAccount, useCurrentUser } from "@coinbase/cdp-hooks";

  function CreateSmartAccount() {
    const { createEvmSmartAccount } = useCreateEvmSmartAccount();
    const { currentUser } = useCurrentUser();

    const handleCreate = async () => {
      // Use the first EOA as the owner
      const ownerAddress = currentUser?.evmAccountObjects?.[0]?.address;

      if (!ownerAddress) {
        console.error("No EOA account found. Create an EOA first.");
        return;
      }

      try {
        const account = await createEvmSmartAccount({ ownerAddress });
        console.log("New Smart Account created:", account.address);
        console.log("Owner:", account.ownerAddresses[0]);
        console.log("Created at:", new Date(account.createdAt).toLocaleDateString());
      } catch (error) {
        console.error("Failed to create smart account:", error);
      }
    };

    return (
      <div>
        <h3>Your Smart Accounts ({currentUser?.evmSmartAccountObjects?.length || 0}/10)</h3>
        <button onClick={handleCreate}>
          Create New Smart Account
        </button>
      </div>
    );
  }
  ```

  ```tsx Solana Account theme={null}
  import { useCreateSolanaAccount, useCurrentUser } from "@coinbase/cdp-hooks";

  function CreateSolanaAccount() {
    const { createSolanaAccount } = useCreateSolanaAccount();
    const { currentUser } = useCurrentUser();

    const handleCreate = async () => {
      try {
        const account = await createSolanaAccount();
        console.log("New Solana account created:", account.address);
        console.log("Created at:", new Date(account.createdAt).toLocaleDateString());
      } catch (error) {
        console.error("Failed to create account:", error);
      }
    };

    return (
      <div>
        <h3>Your Solana Accounts ({currentUser?.solanaAccountObjects?.length || 0}/10)</h3>
        <button onClick={handleCreate}>
          Create New Solana Account
        </button>
      </div>
    );
  }
  ```
</CodeGroup>

### Using Core SDK

For non-React applications, use the core SDK functions:

<CodeGroup>
  ```typescript EVM EOA Account theme={null}
  import { createEvmEoaAccount } from "@coinbase/cdp-core";

  // Create a new EOA account
  const account = await createEvmEoaAccount();

  console.log("Address:", account.address);
  console.log("Created:", new Date(account.createdAt).toLocaleDateString());
  ```

  ```typescript EVM Smart Account theme={null}
  import { createEvmSmartAccount, getCurrentUser } from "@coinbase/cdp-core";

  // Get the current user to find an EOA owner
  const user = await getCurrentUser();
  const ownerAddress = user?.evmAccountObjects?.[0]?.address;

  if (!ownerAddress) {
    throw new Error("No EOA account found. Create an EOA first.");
  }

  // Create a new Smart Account
  const account = await createEvmSmartAccount({ ownerAddress });

  console.log("Address:", account.address);
  console.log("Owners:", account.ownerAddresses);
  console.log("Created:", new Date(account.createdAt).toLocaleDateString());
  ```

  ```typescript Solana Account theme={null}
  import { createSolanaAccount } from "@coinbase/cdp-core";

  // Create a new Solana account
  const account = await createSolanaAccount();

  console.log("Address:", account.address);
  console.log("Created:", new Date(account.createdAt).toLocaleDateString());
  ```
</CodeGroup>

## Accessing account data

All user accounts are available through the `currentUser` object with metadata including creation timestamps and ownership information.

### List all accounts

```tsx theme={null}
import { useCurrentUser } from "@coinbase/cdp-hooks";

function AccountList() {
  const { currentUser } = useCurrentUser();

  if (!currentUser) return <div>Please sign in</div>;

  return (
    <div>
      <h2>EVM EOA Accounts</h2>
      {currentUser.evmAccountObjects?.map((account, index) => (
        <div key={account.address}>
          <p>Account {index + 1}: {account.address}</p>
          <p>Created: {new Date(account.createdAt).toLocaleDateString()}</p>
        </div>
      ))}

      <h2>EVM Smart Accounts</h2>
      {currentUser.evmSmartAccountObjects?.map((account, index) => (
        <div key={account.address}>
          <p>Account {index + 1}: {account.address}</p>
          <p>Owners: {account.ownerAddresses.join(", ")}</p>
          <p>Created: {new Date(account.createdAt).toLocaleDateString()}</p>
        </div>
      ))}

      <h2>Solana Accounts</h2>
      {currentUser.solanaAccountObjects?.map((account, index) => (
        <div key={account.address}>
          <p>Account {index + 1}: {account.address}</p>
          <p>Created: {new Date(account.createdAt).toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  );
}
```

### Account object properties

#### EVM EOA

| Property    | Type     | Description                                     |
| ----------- | -------- | ----------------------------------------------- |
| `address`   | `string` | The blockchain address of the account           |
| `createdAt` | `string` | ISO 8601 timestamp when the account was created |

#### EVM Smart Account

| Property         | Type       | Description                                        |
| ---------------- | ---------- | -------------------------------------------------- |
| `address`        | `string`   | The blockchain address of the account              |
| `createdAt`      | `string`   | ISO 8601 timestamp when the account was created    |
| `ownerAddresses` | `string[]` | Array of EOA addresses that own this Smart Account |

#### Solana Account

| Property    | Type     | Description                                     |
| ----------- | -------- | ----------------------------------------------- |
| `address`   | `string` | The blockchain address of the account           |
| `createdAt` | `string` | ISO 8601 timestamp when the account was created |

## Working with multiple accounts

### Selecting accounts for transactions

When sending transactions, specify which account to use:

<CodeGroup>
  ```tsx EVM Transaction theme={null}
  import { useEvmAddress, useCurrentUser } from "@coinbase/cdp-hooks";
  import { SendEvmTransactionButton } from "@coinbase/cdp-react";
  import { useMemo, useState } from "react";

  function MultiAccountTransaction() {
    const { currentUser } = useCurrentUser();
    const [selectedAccountIndex, setSelectedAccountIndex] = useState(0);

    // Sort accounts by creation date (oldest first)
    const sortedAccounts = useMemo(() => {
      return currentUser?.evmAccountObjects?.slice().sort((a, b) =>
        new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      ) || [];
    }, [currentUser?.evmAccountObjects]);

    const selectedAccount = sortedAccounts[selectedAccountIndex];

    return (
      <div>
        <h3>Select Account</h3>
        <select
          value={selectedAccountIndex}
          onChange={(e) => setSelectedAccountIndex(Number(e.target.value))}
        >
          {sortedAccounts.map((account, index) => (
            <option key={account.address} value={index}>
              Account {index + 1}: {account.address.slice(0, 6)}...{account.address.slice(-4)}
            </option>
          ))}
        </select>

        {selectedAccount && (
          <SendEvmTransactionButton
            account={selectedAccount.address}
            network="base-sepolia"
            transaction={{
              to: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
              value: 1000000000000000n,
              chainId: 84532,
              type: "eip1559",
            }}
            onSuccess={(hash) => console.log("Transaction sent:", hash)}
            onError={(error) => console.error("Transaction failed:", error)}
          />
        )}
      </div>
    );
  }
  ```

  ```tsx Solana Transaction theme={null}
  import { useCurrentUser } from "@coinbase/cdp-hooks";
  import { SendSolanaTransactionButton } from "@coinbase/cdp-react";
  import { useMemo, useState } from "react";

  function MultiAccountSolanaTransaction() {
    const { currentUser } = useCurrentUser();
    const [selectedAccountIndex, setSelectedAccountIndex] = useState(0);

    // Sort accounts by creation date (oldest first)
    const sortedAccounts = useMemo(() => {
      return currentUser?.solanaAccountObjects?.slice().sort((a, b) =>
        new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      ) || [];
    }, [currentUser?.solanaAccountObjects]);

    const selectedAccount = sortedAccounts[selectedAccountIndex];

    return (
      <div>
        <h3>Select Solana Account</h3>
        <select
          value={selectedAccountIndex}
          onChange={(e) => setSelectedAccountIndex(Number(e.target.value))}
        >
          {sortedAccounts.map((account, index) => (
            <option key={account.address} value={index}>
              Account {index + 1}: {account.address.slice(0, 6)}...{account.address.slice(-4)}
            </option>
          ))}
        </select>

        {selectedAccount && (
          <SendSolanaTransactionButton
            account={selectedAccount.address}
            network="solana-devnet"
            transaction="base64-encoded-solana-transaction"
            onSuccess={(signature) => console.log("Transaction sent:", signature)}
            onError={(error) => console.error("Transaction failed:", error)}
          />
        )}
      </div>
    );
  }
  ```

  ```tsx Smart Account UserOp theme={null}
  import { useSendUserOperation, useCurrentUser } from "@coinbase/cdp-hooks";
  import { useMemo, useState } from "react";

  function MultiSmartAccountTransaction() {
    const { sendUserOperation, status } = useSendUserOperation();
    const { currentUser } = useCurrentUser();
    const [selectedAccountIndex, setSelectedAccountIndex] = useState(0);

    // Sort accounts by creation date (oldest first)
    const sortedAccounts = useMemo(() => {
      return currentUser?.evmSmartAccountObjects?.slice().sort((a, b) =>
        new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      ) || [];
    }, [currentUser?.evmSmartAccountObjects]);

    const selectedSmartAccount = sortedAccounts[selectedAccountIndex];

    const handleSend = async () => {
      if (!selectedSmartAccount) return;

      try {
        const result = await sendUserOperation({
          evmSmartAccount: selectedSmartAccount.address,
          network: "base-sepolia",
          calls: [{
            to: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            value: 1000000000000000n,
            data: "0x",
          }],
        });
        console.log("UserOp hash:", result.userOperationHash);
      } catch (error) {
        console.error("Failed:", error);
      }
    };

    return (
      <div>
        <h3>Select Smart Account</h3>
        <select
          value={selectedAccountIndex}
          onChange={(e) => setSelectedAccountIndex(Number(e.target.value))}
        >
          {sortedAccounts.map((account, index) => (
            <option key={account.address} value={index}>
              Smart Account {index + 1}: {account.address.slice(0, 6)}...{account.address.slice(-4)}
            </option>
          ))}
        </select>

        <button onClick={handleSend} disabled={status === "pending"}>
          {status === "pending" ? "Sending..." : "Send User Operation"}
        </button>
      </div>
    );
  }
  ```
</CodeGroup>

## Use cases

Multiple accounts enable various organizational and functional patterns:

* **Organizing funds by purpose**: Separate accounts for personal, business, and savings to keep funds organized
* **Separating assets by network**: Different accounts optimized for specific networks or token types
* **Managing different identities**: Maintain separate blockchain identities for public and private transactions
* **Separating NFT collections**: Organize NFTs across different accounts by collection, purpose, or value
* **Different trading strategies**: Separate accounts for different trading approaches or risk profiles
* **Multi-purpose fund management**: Organize funds across multiple accounts based on liquidity needs
* **Smart account configurations**: Different Smart Account setups for different use cases (e.g., sponsored vs. non-sponsored flows)
* **Managing spending policies**: Separate Smart Accounts with different spending permissions and rules

<Warning>
  **Account limits**: Users are limited to 10 accounts of each type (i.e. 30 accounts total). Always check the current count before attempting to create new accounts.
</Warning>

<Note>
  **Smart Account owners**: Each Smart Account requires a unique EOA owner; you cannot create multiple Smart Accounts with the same EOA. Each of the user's EOA accounts can own one Smart Account, creating a one-to-one relationship.
</Note>

## Reference

| Resource                                                                                                                                                             | Description                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [`useCreateEvmEoaAccount`](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/hooks/src/hooks/useCreateEvmEoaAccount.ts)     | React hook to create EVM EOA accounts              |
| [`useCreateEvmSmartAccount`](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/hooks/src/hooks/useCreateEvmSmartAccount.ts) | React hook to create EVM Smart Accounts            |
| [`useCreateSolanaAccount`](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/hooks/src/hooks/useCreateSolanaAccount.ts)     | React hook to create Solana accounts               |
| [`createEvmEoaAccount`](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/core/src/actions/createEvmEoaAccount.ts)          | Core SDK function to create EVM EOA accounts       |
| [`createEvmSmartAccount`](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/core/src/actions/createEvmSmartAccount.ts)      | Core SDK function to create EVM Smart Accounts     |
| [`createSolanaAccount`](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/core/src/actions/createSolanaAccount.ts)          | Core SDK function to create Solana accounts        |
| [`useCurrentUser`](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/hooks/src/hooks.ts#L568)                               | React hook to access current user and all accounts |
| [User type](https://github.com/coinbase/cdp-web/blob/c7d5e5c5499e30934911d05e26fd2e9921b7e0b3/packages/core/src/types.ts#L189)                                       | TypeScript type definitions for user accounts      |

## What to read next

<CardGroup>
  <Card title="Account Manager" icon="user-gear" href="/embedded-wallets/account-manager">
    Learn about the built-in account management UI component
  </Card>

  <Card title="Smart Accounts" icon="microchip" href="/embedded-wallets/evm-features/smart-accounts">
    Explore Smart Account features and capabilities
  </Card>

  <Card title="React Hooks" icon="code" href="/embedded-wallets/react-hooks">
    View all available hooks for embedded wallets
  </Card>

  <Card title="Best Practices" icon="lightbulb" href="/embedded-wallets/best-practices">
    Learn best practices for embedded wallet integration
  </Card>
</CardGroup>

