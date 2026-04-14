# npm
npm install @coinbase/cdp-core @coinbase/cdp-hooks
```

### Enable smart accounts

Configure the `CDPHooksProvider` to create a smart account for new users on sign in.

```tsx theme={null}
import { CDPHooksProvider } from "@coinbase/cdp-hooks";

function App() {
  return (
    <CDPHooksProvider
      config={{
        projectId: "your-project-id",
        ethereum: {
          createOnLogin: "smart", // Automatically create Smart Accounts
        }
      }}
    >
      <YourApp />
    </CDPHooksProvider>
  );
}
```

* When `ethereum.createOnLogin` is set to `"smart"`, new users receive both an EOA and a smart account.

Other config keys supported by the SDK provider:

* `basePath` (API base URL override)
* `useMock` (local mock mode)
* `debugging` (verbose logging)

## Access the user's smart account

Use `useCurrentUser` to access the authenticated user's accounts. The first smart account is available as `currentUser.evmSmartAccounts?.[0]`.

```tsx theme={null}
import { useCurrentUser } from "@coinbase/cdp-hooks";

function SmartAccountBadge() {
  const { currentUser } = useCurrentUser();
  const smartAccount = currentUser?.evmSmartAccounts?.[0];
  if (!currentUser) return <div>Please sign in</div>;

  return (
    <div>
      <p>Owner EOA: {currentUser.evmAccounts?.[0]}</p>
      {smartAccount && <p>Smart Account: {smartAccount}</p>}
    </div>
  );
}
```

Alternatively, use `useEvmAddress()` to get the primary EVM address; it returns the smart account if one exists, otherwise the EOA.

## Send a user operation

Smart accounts submit ERC-4337 user operations rather than standard EOA transactions.

Use `useSendUserOperation` to submit one or more calls. This hook returns `status`, `data`, and `error` values which you can use to track the status of the user operation.

<Tip>
  For gas sponsorship with a [Paymaster](#gas-sponsorship-with-paymaster), either set `useCdpPaymaster: true` (uses the CDP Paymaster on Base) or provide a custom `paymasterUrl`.
  CDP Paymaster only supports Base. For other networks, any [ERC-7677](https://eips.ethereum.org/EIPS/eip-7677) compliant Paymaster is compatible with CDP Smart accounts.
</Tip>

```tsx theme={null}
import { useSendUserOperation, useCurrentUser } from "@coinbase/cdp-hooks";

function SendUserOperation() {
  const { sendUserOperation, status, data, error } = useSendUserOperation();
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
        // Optional gas sponsorship
        // useCdpPaymaster: true,
        // or provide your own paymasterUrl
        // paymasterUrl: "https://your-paymaster.example.com",
      });

      console.log("User Operation Hash:", result.userOperationHash);
    } catch (error) {
      console.error("Failed to send user operation:", error);
    }
  };

  return (
    <div>
      {status === "idle" && <p>Ready to send user operation</p>}
      
      {status === "pending" && (
        <div>
          <p>User operation pending...</p>
          {data && <p>User Op Hash: {data.userOpHash}</p>}
        </div>
      )}
      
      {status === "success" && data && (
        <div>
          <p>User operation successful!</p>
          <p>Transaction Hash: {data.transactionHash}</p>
          <p>Status: {data.status}</p>
        </div>
      )}
      
      {status === "error" && (
        <div>
          <p>User operation failed</p>
          <p>Error: {error?.message}</p>
        </div>
      )}
      
      <button onClick={handleSendUserOperation} disabled={status === "pending"}>
        {status === "pending" ? "Sending..." : "Send User Operation"}
      </button>
    </div>
  );
}
```

### Batch calls

Provide multiple `calls` to batch actions in a single user operation. Calls execute in order and revert atomically on failure.

```tsx theme={null}
const { userOperationHash } = await sendUserOperation({
  evmSmartAccount: smartAccount,
  network: "base-sepolia",
  calls: [
    { to: addr1, value: 100000000000000000n },
    { to: addr2, value: 50000000000000000n },
  ],
});
```

### Encode contract calls

To interact with contracts, pass `data` using an ABI-encoded payload. This example encodes an ERC-20 `transfer` using `viem`:

```tsx theme={null}
import { encodeFunctionData } from "viem";

const erc20Abi = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "value", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
];

const data = encodeFunctionData({
  abi: erc20Abi as const,
  functionName: "transfer",
  args: [recipient, 1_000_000n], // 1 USDC assuming 6 decimals
});

await sendUserOperation({
  evmSmartAccount: smartAccount,
  network: "base-sepolia",
  calls: [
    {
      to: usdcAddress,
      data,
      value: 0n,
    },
  ],
});
```

## Using non-Base networks

Smart accounts can send user operations on the following networks:

| Network   | Mainnet | Testnet          |
| --------- | ------- | ---------------- |
| Base      | ✓       | ✓ (Base Sepolia) |
| Arbitrum  | ✓       |                  |
| Optimism  | ✓       |                  |
| Zora      | ✓       |                  |
| Polygon   | ✓       |                  |
| BNB Chain | ✓       |                  |
| Avalanche | ✓       |                  |
| Ethereum  | ✓       | ✓ (Sepolia)      |

<Note>
  **Feature availability:** While smart accounts support user operations across all these networks, some features like token transfers, swaps, and funding are only available on specific networks. For the complete feature support matrix, see the [CDP SDK documentation](https://github.com/coinbase/cdp-sdk).
</Note>

<Warning>
  **Gas sponsorship:** [`useCdpPaymaster`](#gas-sponsorship-with-paymaster) only works on Base networks. For other chains, provide your own [ERC-7677](https://eips.ethereum.org/EIPS/eip-7677)-compatible paymaster via the `paymasterUrl` parameter. See the Ethereum example below for more details.
</Warning>

Simply specify the `network` parameter for any supported chain. For example:

<CodeGroup>
  ```tsx ethereum theme={null}
  const { userOperationHash } = await sendUserOperation({
    evmSmartAccount: smartAccount,
    network: "ethereum",
    calls: [{
      to: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
      value: 100000000000000000n, // 0.1 ETH
      data: "0x",
    }],
    // Optional: provide your own paymaster for gas sponsorship
    paymasterUrl: "https://your-paymaster.example.com",
  });
  ```

  ```tsx polygon theme={null}
  const { userOperationHash } = await sendUserOperation({
    evmSmartAccount: smartAccount,
    network: "polygon",
    calls: [{
      to: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
      value: 100000000000000000n, // 0.1 MATIC
      data: "0x",
    }],
  });
  ```

  ```tsx arbitrum-sepolia theme={null}
  const { userOperationHash } = await sendUserOperation({
    evmSmartAccount: smartAccount,
    network: "arbitrum-sepolia",
    calls: [{
      to: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
      value: 10000000000000000n, // 0.01 ETH
      data: "0x",
    }],
  });
  ```
</CodeGroup>

## Gas sponsorship with paymaster

Use a paymaster to sponsor gas so users can transact without holding ETH.

* Add `paymasterUrl` to `sendUserOperation`
* Or set `useCdpPaymaster: true` to use the CDP Paymaster

Learn more about our [Paymaster](/paymaster/introduction/welcome) or see the [Paymaster Quickstart](/paymaster/guides/quickstart).

```tsx theme={null}
await sendUserOperation({
  evmSmartAccount: smartAccount,
  network: "base-sepolia",
  calls: [{ to: recipient, value: 10n ** 15n }],
  paymasterUrl: "https://your-paymaster.example.com",
});
```

<Note>
  Questions? Contact us in the #embedded-wallets channel on [Discord](https://discord.gg/cdp).
</Note>

## Reference

| Resource                                                                                                                                        | Description                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [`useCurrentUser`](https://github.com/coinbase/cdp-web/blob/d2bf487d1ba29cfbeec73123a14b104a35819368/packages/hooks/src/hooks.ts#L362)          | Get the current authenticated user                       |
| [`useEvmAddress`](https://github.com/coinbase/cdp-web/blob/d2bf487d1ba29cfbeec73123a14b104a35819368/packages/hooks/src/hooks.ts#L447)           | Primary EVM address (Smart Account if present, else EOA) |
| [`useSendUserOperation`](https://github.com/coinbase/cdp-web/blob/d2bf487d1ba29cfbeec73123a14b104a35819368/packages/hooks/src/hooks.ts#L1118)   | Send a user operation; hook returns status/data          |
| [`sendUserOperationOptions`](https://github.com/coinbase/cdp-web/blob/d2bf487d1ba29cfbeec73123a14b104a35819368/packages/core/src/types.ts#L403) | Options for sending a user operation                     |
| [`sendUserOperationResult`](https://github.com/coinbase/cdp-web/blob/d2bf487d1ba29cfbeec73123a14b104a35819368/packages/core/src/types.ts#L419)  | Result fields for sendUserOperation                      |
| [`ethereum.createOnLogin`](https://github.com/coinbase/cdp-web/blob/d2bf487d1ba29cfbeec73123a14b104a35819368/packages/core/src/types.ts#L47)    | Config: "eoa" or "smart"                                 |
| [User type](https://github.com/coinbase/cdp-web/blob/main/packages/core/src/types.ts#L56)                                                       | `user.evmAccounts[]`, `user.evmSmartAccounts[]`          |
| [Hooks README](https://github.com/coinbase/cdp-web/blob/main/packages/hooks/README.md)                                                          | Package overview and usage                               |

## What to read next

* [Spend Permissions](/embedded-wallets/evm-features/spend-permissions)
* [React Hooks](/embedded-wallets/react-hooks)
* [Paymaster](/paymaster/introduction/welcome)
* [EIP-7702 Delegation](/embedded-wallets/evm-features/eip-7702-delegation)

