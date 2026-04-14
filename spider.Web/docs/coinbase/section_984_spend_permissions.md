# Spend Permissions
Source: https://docs.cdp.coinbase.com/embedded-wallets/evm-features/spend-permissions



## Overview

Spend Permissions let you designate a trusted spender that can spend tokens on behalf of your [Smart Account](/embedded-wallets/evm-features/smart-accounts). This enables use cases like subscription payments, agentic payments, algorithmic trading, automated payouts, and allowance management.

Spend Permissions utilize the [Spend Permission Manager contract](https://github.com/coinbase/spend-permissions) deployed on Base and [other networks](#supported-networks).

## Use cases

* **Subscription payments** - Enable recurring payments for SaaS, content subscriptions, or membership fees
* **Agentic payments** - Delegate your actions to an agent with spending limits for autonomous operations
* **Algorithmic trading** - Allow trading bots to execute trades within predefined limits
* **Automated payouts** - Schedule regular distributions or reward payments
* **Allowance management** - Give team members or family controlled access to funds

## How it works

There are two parties involved in a spend permission:

* **Account** - The smart account that creates the spend permission and approves it onchain.
* **Spender** - The entity that can spend tokens on behalf of the account within the limits defined by a spend permission. Can be a Smart Account or a regular account.

The CDP Embedded Wallet SDK makes it easy to work with spend permissions as the **account owner**, offering methods to create and manage permissions. If you're the **spender**, see [Using a spend permission](#for-spenders-using-permissions).

## Anatomy of a spend permission

These are the main components of a spend permission:

* **Spender** - The entity that can spend tokens on behalf of the account.
* **Token** - The token that the spend permission is for, and the amount of that token that the spender is allowed to spend.
* **Time period** - The time period for which the spend permission is valid.
* **Salt** - A random value used to differentiate between spend permissions with the same parameters. The SDK will generate a random salt for you, but you can also specify your own.
* **Extra Data** - Arbitrary data that can be used to store additional information about the spend permission.

See the following sections for more details on the main components.

### Spender

The spender is specified in the `spender` field of the spend permission. It can be the address of any account, whether it's a Smart Account or a regular account.

### Token

The token is specified in the `token` field of the spend permission, and the amount allowed to spend is specified in the `allowance` field.

Spend permissions support both native tokens and ERC-20 tokens. When using the CDP SDK, you have two options for specifying tokens:

1. **Convenient shortcuts** - Use `"eth"` for native ETH or `"usdc"` for USDC, and the SDK will handle the conversion to the correct token address. This shortcut is only supported on Base or Base Sepolia.
2. **ERC-20 contract addresses** - For other tokens, specify the token contract address as a string (e.g., `"0x4200000000000000000000000000000000000006"` for WETH).

The amount allowed to spend is specified in the `allowance` field, using the smallest unit of the token. For example, if the token is ETH, the allowance is specified in wei, and if the token is USDC, the allowance is specified in the smallest unit of USDC (6 decimals).

### Time period

The time period is specified using the `periodInDays` field for simple day-based periods, or the `period`, `start` and `end` fields for more complex time controls.

The `periodInDays` field provides a convenient way to specify common time periods (e.g., `periodInDays: 1` for daily limits, `periodInDays: 7` for weekly limits).

For more advanced control, the `start` and `end` fields specify when the spend permission is valid. This means that the spender can spend the amount specified in the `allowance` field after the `start` time and before the `end` time; attempting to spend outside of this time range will fail.

<Info>
  The `period` field specifies a rolling window of time in seconds in which the spender can spend the amount specified in the `allowance` field. This allows you specify things like "the spender can spend up to 0.00001 ETH per day" or "the spender can spend up to 100 USDC per week".
</Info>

## Prerequisites

<Warning>
  Smart Accounts must have spend permissions enabled at the time of creation. You cannot create spend permissions on accounts that were created without spend permissions enabled.
</Warning>

Install the required packages:

<CodeGroup>
  ```bash npm theme={null}
  npm install @coinbase/cdp-react @coinbase/cdp-core @coinbase/cdp-hooks
  ```

  ```bash pnpm theme={null}
  pnpm add @coinbase/cdp-react @coinbase/cdp-core @coinbase/cdp-hooks
  ```

  ```bash yarn theme={null}
  yarn add @coinbase/cdp-react @coinbase/cdp-core @coinbase/cdp-hooks
  ```
</CodeGroup>

<Tip>
  If you're new to Embedded Wallets, start with the [Quickstart](/embedded-wallets/quickstart) and [React Hooks](/embedded-wallets/react-hooks) first.
</Tip>

Configure the `CDPHooksProvider` to enable spend permissions for smart accounts:

```tsx theme={null}
import { CDPHooksProvider } from "@coinbase/cdp-hooks";

function App() {
  return (
    <CDPHooksProvider
      config={{
        projectId: "your-project-id",
        ethereum: {
          createOnLogin: "smart",
          enableSpendPermissions: true, // Enable spend permissions for Smart Accounts
        }
      }}
    >
      <YourApp />
    </CDPHooksProvider>
  );
}
```

When `enableSpendPermissions` is set to `true`, the created smart accounts will support spend permissions functionality.

## Create a spend permission

Use `useCreateSpendPermission` to create a spend permission that allows a spender to withdraw tokens from the embedded wallet within defined limits:

```tsx theme={null}
import { useCreateSpendPermission } from "@coinbase/cdp-hooks";
import { parseUnits } from "viem";

function CreateSpendPermission() {
  const { createSpendPermission, status, data, error } = useCreateSpendPermission();

  const handleCreatePermission = async () => {
    try {
      const result = await createSpendPermission({
        network: "base-sepolia",
        spender: "0x1399BE2B2E4186C209617053822C67173E8DFe5c", // Address that can spend tokens
        token: "usdc", // Supports "usdc", "eth", or token address
        allowance: parseUnits("10", 6), // 10 USDC (6 decimals)
        periodInDays: 7, // Weekly limit
        useCdpPaymaster: true, // Use CDP Paymaster for gas sponsorship
      });

      console.log("Spend Permission Created! User Operation Hash:", result.userOperationHash);
    } catch (error) {
      console.error("Failed to create spend permission:", error);
    }
  };

  return (
    <div>
      {status === "idle" && <p>Ready to create spend permission</p>}
      
      {status === "pending" && (
        <div>
          <p>Creating spend permission...</p>
          {data && <p>User Op Hash: {data.userOpHash}</p>}
        </div>
      )}
      
      {status === "success" && data && (
        <div>
          <p>Spend permission created successfully!</p>
          <p>User Operation Hash: {data.userOpHash}</p>
          <p>Transaction Hash: {data.transactionHash}</p>
          <p>Status: {data.status}</p>
        </div>
      )}
      
      {status === "error" && (
        <div>
          <p>Failed to create spend permission</p>
          <p>Error: {error?.message}</p>
        </div>
      )}
      
      <button onClick={handleCreatePermission} disabled={status === "pending"}>
        {status === "pending" ? "Creating..." : "Create Spend Permission"}
      </button>
    </div>
  );
}
```

<Tip>
  Creating a spend permission is a user operation that requires gas. You can use the CDP Paymaster on Base networks by setting `useCdpPaymaster: true`, or provide your own `paymasterUrl` for gas sponsorship.
</Tip>

### Common patterns

Here are some common patterns for creating spend permissions:

```tsx theme={null}
import { useCreateSpendPermission } from "@coinbase/cdp-hooks";
import { parseUnits, parseEther } from "viem";

// USDC spend permission with daily limit
const usdcPermission = await createSpendPermission({
  network: "base",
  spender: "0x...",
  token: "usdc", // Convenient shortcut for USDC
  allowance: parseUnits("100", 6), // 100 USDC (6 decimals)
  periodInDays: 1, // Daily limit
  useCdpPaymaster: true,
});

// ETH spend permission with weekly limit
const ethPermission = await createSpendPermission({
  network: "base-sepolia",
  spender: "0x...",
  token: "eth", // Convenient shortcut for native ETH
  allowance: parseEther("0.1"), // 0.1 ETH
  periodInDays: 7, // Weekly limit
  paymasterUrl: "https://your-paymaster.example.com", // Custom paymaster
});

// Custom token with monthly limit
const customTokenPermission = await createSpendPermission({
  network: "base-sepolia",
  spender: "0x...",
  token: "0x4200000000000000000000000000000000000006", // WETH address
  allowance: parseEther("5"), // 5 WETH
  periodInDays: 30, // Monthly limit
  useCdpPaymaster: true,
});
```

## List spend permissions

Use `useListSpendPermissions` to retrieve spend permissions. The hook automatically detects and lists permissions for the authenticated user's smart account.

<Info>
  The `useListSpendPermissions` hook automatically lists spend permissions for your current Smart Account.

  The hook accepts an optional configuration object:

  * `network`: The network to fetch spend permissions on. Defaults to "base-sepolia"
  * `pageToken`: Token for pagination to fetch the next page of results

  The returned data contains:

  * `spendPermissions`: Array of `SpendPermissionResponseObject` where each object contains:
    * `permission`: The actual spend permission details
    * `permissionHash`: Unique identifier for the permission
    * `revoked`: Boolean indicating if the permission has been revoked
    * `createdAt`: Timestamp when the permission was created
    * `network`: The network where the permission exists
  * `hasNextPage`: Boolean indicating if more results are available
  * `nextPageToken`: Token to fetch the next page of results

  The hook also returns:

  * `refetch`: Function to refresh the list of spend permissions
  * `status`: Current status ("idle" | "pending" | "success" | "error")
  * `error`: Error object if the request fails
</Info>

```tsx theme={null}
import { useListSpendPermissions, useCurrentUser } from "@coinbase/cdp-hooks";
import { useState } from "react";

function ListSpendPermissions() {
  const { currentUser } = useCurrentUser();
  const [currentPageToken, setCurrentPageToken] = useState<string | undefined>(undefined);
  
  const { 
    refetch: listSpendPermissionsRefetch, 
    data, 
    error, 
    status 
  } = useListSpendPermissions({
    pageToken: currentPageToken,
  });

  const hasSmartAccount = !!currentUser?.evmSmartAccounts?.[0];

  const fetchNextPage = () => {
    if (!data?.nextPageToken) return;
    setCurrentPageToken(data.nextPageToken);
  };

  return (
    <div>
      <button 
        onClick={listSpendPermissionsRefetch}
        disabled={!hasSmartAccount}
      >
        Refresh Spend Permissions
      </button>
      
      {!hasSmartAccount && (
        <p style={{ color: 'red' }}>
          You need a Smart Account to list spend permissions.
        </p>
      )}

      {status === "idle" && (
        <p>No spend permissions listing in progress</p>
      )}
      
      {status === "pending" && (
        <p>Listing spend permissions...</p>
      )}
      
      {status === "success" && data && (
        <div>
          <h3>Spend permissions listed successfully!</h3>
          {data.spendPermissions?.map((spendPermission) => (
            <div key={spendPermission.permissionHash}>
              <p>Permission Hash: {spendPermission.permissionHash}</p>
              <p>Spender: {spendPermission.permission.spender}</p>
              <p>Token: {spendPermission.permission.token}</p>
              <p>Allowance: {spendPermission.permission.allowance}</p>
              <p>Period: {spendPermission.permission.period} seconds</p>
              <p>Revoked: {spendPermission.revoked ? "Yes" : "No"}</p>
              <p>Created: {new Date(spendPermission.createdAt).toLocaleString()}</p>
            </div>
          ))}
          
          {data.hasNextPage && (
            <button onClick={fetchNextPage}>
              Load More Permissions
            </button>
          )}
        </div>
      )}
      
      {status === "error" && (
        <div>
          <p style={{ color: 'red' }}>Failed to list spend permissions</p>
          <p>Error: {error?.message}</p>
        </div>
      )}
    </div>
  );
}
```

## Revoke spend permissions

Use `useRevokeSpendPermission` to revoke an existing spend permission. The hook returns `status`, `data`, and `error` values for tracking the revocation process:

```tsx theme={null}
import { useRevokeSpendPermission } from "@coinbase/cdp-hooks";
import { useState } from "react";

function RevokeSpendPermission({ permissionToRevoke }) {
  const { revokeSpendPermission, status, data, error } = useRevokeSpendPermission();

  const handleRevokePermission = async () => {
    if (!permissionToRevoke?.permissionHash) return;

    try {
      // This will automatically start tracking the user operation status
      const result = await revokeSpendPermission({
        network: "base-sepolia",
        permissionHash: permissionToRevoke.permissionHash,
        useCdpPaymaster: true, // Use CDP Paymaster on Base (enabled by default on Base Sepolia)
        // Or provide a custom paymaster URL:
        // paymasterUrl: "https://your-paymaster.example.com",
      });

      console.log("Revoke initiated! User Operation Hash:", result.userOperationHash);
    } catch (error) {
      console.error("Failed to revoke spend permission:", error);
    }
  };

  return (
    <div>
      {status === "idle" && <p>Ready to revoke permission</p>}
      
      {status === "pending" && (
        <div>
          <p>Revoking spend permission...</p>
          {data && <p>User Op Hash: {data.userOpHash}</p>}
        </div>
      )}
      
      {status === "success" && data && (
        <div>
          <p>Spend permission revoked successfully!</p>
          <p>User Operation Hash: {data.userOpHash}</p>
          <p>Transaction Hash: {data.transactionHash}</p>
          <p>Status: {data.status}</p>
        </div>
      )}
      
      {status === "error" && (
        <div>
          <p>Failed to revoke spend permission</p>
          <p>Error: {error?.message}</p>
        </div>
      )}
      
      <button onClick={handleRevokePermission} disabled={status === "pending"}>
        {status === "pending" ? "Revoking..." : "Revoke Spend Permission"}
      </button>
    </div>
  );
}
```

<Tip>
  Revoking a spend permission is a user operation that requires gas. You can use the CDP Paymaster on Base networks by setting `useCdpPaymaster: true`, or provide your own `paymasterUrl` for gas sponsorship.
</Tip>

<Info>
  The `revokeSpendPermission` function returns:

  * `userOperationHash`: The hash of the user operation that revokes the permission

  To track the status of the revocation, you can:

  1. Call `useWaitForUserOperation()` with the user operation hash to wait for the revocation to complete.
</Info>

### Complete example with list and revoke

Here's a complete example that lists permissions and allows revoking specific ones:

<Accordion title="Click here to view the complete example">
  <CodeGroup>
    ```tsx theme={null}
    import { useListSpendPermissions, useRevokeSpendPermission, useCurrentUser } from "@coinbase/cdp-hooks";
    import { useState } from "react";

    function ManageSpendPermissions() {
      const { currentUser } = useCurrentUser();
      const { 
        refetch: listSpendPermissionsRefetch,
        data: listData,
        error: listError,
        status: listStatus
      } = useListSpendPermissions();
      
      const { 
        revokeSpendPermission,
        data: revokeData,
        error: revokeError,
        status: revokeStatus
      } = useRevokeSpendPermission();
      
      const [selectedPermissionHash, setSelectedPermissionHash] = useState<string>("");
      const hasSmartAccount = !!currentUser?.evmSmartAccounts?.[0];

      const handleRevoke = async (permissionHash: string) => {
        setSelectedPermissionHash(permissionHash);
        try {
          await revokeSpendPermission({
            network: "base-sepolia",
            permissionHash,
            useCdpPaymaster: true,
          });
          
          // Refresh the list after successful revocation
          listSpendPermissionsRefetch();
        } catch (error) {
          console.error("Failed to revoke permission:", error);
        }
      };

      return (
        <div>
          <h2>Manage Spend Permissions</h2>
          
          <button 
            onClick={() => listSpendPermissionsRefetch()}
            disabled={!hasSmartAccount || listStatus === "pending"}
          >
            {listStatus === "pending" ? "Loading..." : "Refresh Permissions"}
          </button>

          {!hasSmartAccount && (
            <p style={{ color: 'red' }}>
              You need a Smart Account to manage spend permissions.
            </p>
          )}

          {listStatus === "error" && (
            <p style={{ color: 'red' }}>Error: {listError?.message}</p>
          )}

          {listStatus === "success" && listData?.spendPermissions && (
            <div>
              {listData.spendPermissions.map((spendPermission) => (
                <div key={spendPermission.permissionHash} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
                  <p><strong>Spender:</strong> {spendPermission.permission.spender}</p>
                  <p><strong>Token:</strong> {spendPermission.permission.token}</p>
                  <p><strong>Allowance:</strong> {spendPermission.permission.allowance}</p>
                  <p><strong>Period:</strong> {spendPermission.permission.period} seconds</p>
                  <p><strong>Status:</strong> {spendPermission.revoked ? "Revoked" : "Active"}</p>
                  <p><strong>Created:</strong> {new Date(spendPermission.createdAt).toLocaleString()}</p>
                  
                  {!spendPermission.revoked && (
                    <button 
                      onClick={() => handleRevoke(spendPermission.permissionHash)}
                      disabled={revokeStatus === "pending"}
                    >
                      {revokeStatus === "pending" && selectedPermissionHash === spendPermission.permissionHash 
                        ? "Revoking..." 
                        : "Revoke Permission"}
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {revokeStatus === "success" && revokeData && (
            <p style={{ color: 'green' }}>
              Permission revoked successfully! User Op Hash: {revokeData.userOpHash}
            </p>
          )}
        </div>
      );
    }
    ```
  </CodeGroup>
</Accordion>

## For spenders: Using permissions

Once an embedded wallet creates a spend permission, the designated spender can spend tokens using the CDP APIs as shown here [Using a spend permission](/server-wallets/v2/evm-features/spend-permissions#using-a-spend-permission).

## Check remaining allowance

To check how much of a spend permission's allowance remains in the current period, query the `getCurrentPeriod` function on the Spend Permission Manager contract.

<Accordion title="Example: Calculate remaining spend allowance">
  ```typescript theme={null}
  import { createPublicClient, http, type Address } from "viem";
  import { baseSepolia } from "viem/chains";

  const SPEND_PERMISSION_MANAGER_ADDRESS = "0xf85210B21cC50302F477BA56686d2019dC9b67Ad";

  const SPEND_PERMISSION_MANAGER_ABI = [
    {
      inputs: [
        {
          components: [
            { name: "account", type: "address" },
            { name: "spender", type: "address" },
            { name: "token", type: "address" },
            { name: "allowance", type: "uint160" },
            { name: "period", type: "uint48" },
            { name: "start", type: "uint48" },
            { name: "end", type: "uint48" },
            { name: "salt", type: "uint256" },
            { name: "extraData", type: "bytes" },
          ],
          name: "spendPermission",
          type: "tuple",
        },
      ],
      name: "getCurrentPeriod",
      outputs: [
        { name: "start", type: "uint48" },
        { name: "end", type: "uint48" },
        { name: "spend", type: "uint160" },
      ],
      stateMutability: "view",
      type: "function",
    },
  ] as const;

  async function getRemainingAllowance(permission: {
    account: Address;
    spender: Address;
    token: Address;
    allowance: bigint;
    period: number;
    start: number;
    end: number;
    salt: bigint;
    extraData: `0x${string}`;
  }) {
    const client = createPublicClient({
      chain: baseSepolia,
      transport: http(),
    });

    const [periodStart, periodEnd, amountSpent] = await client.readContract({
      address: SPEND_PERMISSION_MANAGER_ADDRESS,
      abi: SPEND_PERMISSION_MANAGER_ABI,
      functionName: "getCurrentPeriod",
      args: [permission],
    });

    const remaining = BigInt(permission.allowance) - amountSpent;

    return {
      periodStart,
      periodEnd,
      spent: amountSpent,
      remaining,
    };
  }

  // Usage with a permission from useListSpendPermissions
  const result = await getRemainingAllowance(permission);
  console.log(`Spent: ${result.spent}, Remaining: ${result.remaining}`);
  ```
</Accordion>

## Supported networks

Spend permissions are currently supported on:

<CardGroup>
  <Card title="Testnets" icon="flask">
    Base Sepolia, Ethereum Sepolia
  </Card>

  <Card title="Mainnets" icon="globe">
    Arbitrum, Avalanche, Base, Ethereum, Optimism, Polygon
  </Card>
</CardGroup>

<Info>
  The Spend Permission Manager contract is deployed at `0xf85210B21cC50302F477BA56686d2019dC9b67Ad` on all supported networks.
</Info>

<Note>
  Questions? Contact us in the #embedded-wallets channel on [Discord](https://discord.gg/cdp).
</Note>

## What to read next

* **[Smart Accounts](/embedded-wallets/evm-features/smart-accounts)**: Learn about smart accounts and their capabilities
* **[React Hooks](/embedded-wallets/react-hooks)**: Explore all available hooks for embedded wallets
* **[Paymaster](/paymaster/introduction/welcome)**: Understand gas sponsorship for user operations

