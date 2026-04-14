# Token Swaps
Source: https://docs.cdp.coinbase.com/embedded-wallets/evm-swaps



<Tags />

If you are already using CDP Embedded Wallets, you can turn on onchain swaps for your users without standing up your own routing stack, DEX integrations, or signing flows. Our onchain swap hooks handle the complexity of getting a quote, preparing the swap, and getting it onchain across all supported networks.

## Overview

Swap any ERC-20 token pair with a simple API that handles price discovery, routing, Permit2 signing, and transaction submission. The SDK provides two levels of abstraction:

* **React hooks** (`@coinbase/cdp-hooks`) — reactive state management with automatic on-chain confirmation tracking
* **Core functions** (`@coinbase/cdp-core`) — framework-agnostic async functions for vanilla JS/TS apps

Both approaches support EOA and Smart Account wallets, with optional gas sponsorship via Paymaster.

<CardGroup>
  <Card title="Any ERC-20 Pair" icon="arrow-right-arrow-left">
    Swap between any supported tokens using contract addresses
  </Card>

  <Card title="Price Discovery" icon="chart-line">
    Get indicative prices with fee and slippage estimates before executing
  </Card>

  <Card title="Smart Account Support" icon="wallet">
    Works with both EOAs and ERC-4337 Smart Accounts
  </Card>

  <Card title="Gas Sponsorship" icon="gas-pump">
    Built-in Paymaster support for gasless Smart Account swaps
  </Card>
</CardGroup>

## Get an indicative price

Before executing a swap, fetch a non-binding price estimate. This is a read-only operation that does not modify any on-chain state.

<Tabs>
  <Tab title="React hooks">
    The `useGetSwapPrice` hook automatically fetches when all required parameters are present and the user is signed in. It uses a stale-while-revalidate strategy: when the token pair or network changes, previous data is cleared; when only the amount, slippage, or account changes, previous data is preserved while the new price loads.

    ```tsx [expandable] theme={null}
    import { useGetSwapPrice } from "@coinbase/cdp-hooks";
    import { useId, useState } from "react";

    function SwapPriceDisplay() {
      const inputId = useId();
      const [fromAmount, setFromAmount] = useState("1000000");

      const { data, status, error, refetch, reset } = useGetSwapPrice({
        network: "base",
        fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        toToken: "0x4200000000000000000000000000000000000006",
        fromAmount,
        slippageBps: 100, // 1% max slippage
      });

      return (
        <div>
          <label htmlFor={inputId}>Amount in atomic units</label>
          <input
            id={inputId}
            value={fromAmount}
            onChange={(e) => setFromAmount(e.target.value)}
          />

          {status === "pending" && <p>Loading price...</p>}

          {data?.liquidityAvailable && (
            <div>
              <p>Expected output: {data.toAmount}</p>
              <p>Minimum output: {data.minToAmount}</p>
              {data.totalNetworkFee && <p>Network fee: {data.totalNetworkFee}</p>}
              {data.fees && <p>Fees: {JSON.stringify(data.fees)}</p>}
              {data.issues && <p>Issues: {JSON.stringify(data.issues)}</p>}
            </div>
          )}

          {data && !data.liquidityAvailable && (
            <p>No liquidity available for this pair</p>
          )}

          {error && <p>Error: {error.message}</p>}

          <button onClick={refetch} disabled={status === "pending"}>
            Refresh Price
          </button>
          <button onClick={reset}>
            Clear
          </button>
        </div>
      );
    }
    ```

    You can disable automatic fetching by passing `enabled: false`:

    ```tsx theme={null}
    const { data, refetch } = useGetSwapPrice({
      network: "base",
      fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      toToken: "0x4200000000000000000000000000000000000006",
      fromAmount: "1000000",
      enabled: false, // Only fetch when refetch() is called
    });
    ```
  </Tab>

  <Tab title="Vanilla JS">
    ```typescript [expandable] theme={null}
    import { getSwapPrice } from "@coinbase/cdp-core";

    const price = await getSwapPrice({
      network: "base",
      fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC
      toToken: "0x4200000000000000000000000000000000000006",   // WETH
      fromAmount: "1000000", // 1 USDC (6 decimals)
      slippageBps: 100, // 1% max slippage
    });

    if (price.liquidityAvailable) {
      console.log("Expected output:", price.toAmount);
      console.log("Minimum after slippage:", price.minToAmount);
      console.log("Network fee estimate:", price.totalNetworkFee);

      if (price.issues) {
        console.warn("Preflight issues:", price.issues);
      }
    } else {
      console.log("No liquidity available for this pair");
    }
    ```
  </Tab>
</Tabs>

### Price result

When liquidity is available, the response includes `toAmount` (expected output), `minToAmount` (minimum after slippage), swap `fees`, estimated `totalNetworkFee`, and preflight `issues`. See [`GetSwapPriceResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetSwapPriceResult) for the full type.

When liquidity is not available, the response omits these values altogether. See [`SwapUnavailableResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwapUnavailableResult) for the full type.

<Tip>
  The `issues` field surfaces problems like insufficient balance or allowance **before** you execute. Check this field to show actionable feedback to users.
</Tip>

## Execute a swap

Execute a swap to submit the transaction on-chain. The CDP Swap API atomically quotes, signs the Permit2 permit, simulates, and submits the transaction.

<Tabs>
  <Tab title="React hooks">
    The `useSwap` hook tracks the full lifecycle: submission, on-chain confirmation, and errors. For EOA accounts it waits for a transaction receipt; for Smart Accounts it polls the user operation until completion.

    ```tsx [expandable] theme={null}
    import { useSwap } from "@coinbase/cdp-hooks";

    function ExecuteSwap() {
      const { swap, data, status, error } = useSwap();

      const handleSwap = async () => {
        await swap({
          network: "base",
          fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
          toToken: "0x4200000000000000000000000000000000000006",
          fromAmount: "1000000",
          slippageBps: 100,
        });
      };

      return (
        <div>
          {status === "idle" && (
            <button onClick={handleSwap}>Swap</button>
          )}

          {status === "pending" && (
            <div>
              <p>Swap in progress...</p>
              {data?.type === "evm-eoa" && (
                <p>Tx: {data.transactionHash}</p>
              )}
              {data?.type === "evm-smart" && (
                <p>UserOp: {data.userOpHash}</p>
              )}
            </div>
          )}

          {status === "success" && data && (
            <div>
              <p>Swap confirmed!</p>
              <p>Sold: {data.fromAmount} ({data.fromToken})</p>
              <p>Expected: {data.toAmount} ({data.toToken})</p>
            </div>
          )}

          {status === "error" && (
            <p>Swap failed: {error?.message}</p>
          )}
        </div>
      );
    }
    ```
  </Tab>

  <Tab title="Vanilla JS">
    The `executeSwap` function resolves once the transaction is submitted on-chain (but before it is confirmed). It returns the transaction hash (EOA) or user operation hash (Smart Account). You can then wait for confirmation separately if needed.

    ```typescript [expandable] theme={null}
    import { executeSwap } from "@coinbase/cdp-core";

    try {
      const result = await executeSwap({
        network: "base",
        fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        toToken: "0x4200000000000000000000000000000000000006",
        fromAmount: "1000000",
        slippageBps: 100,
      });

      if (result.type === "evm-eoa") {
        console.log("Transaction hash:", result.transactionHash);
      } else if (result.type === "evm-smart") {
        console.log("User operation hash:", result.userOpHash);
      }

      console.log("From:", result.fromAmount, result.fromToken);
      console.log("To (expected):", result.toAmount, result.toToken);
      console.log("To (minimum):", result.minToAmount);
      console.log("Network fee:", result.totalNetworkFee);
    } catch (err) {
      console.error("Swap failed:", err);
    }
    ```
  </Tab>
</Tabs>

### Swap result

The result is a discriminated union based on account type: `"evm-eoa"` results include a `transactionHash`, while `"evm-smart"` results include a `userOpHash`. Both include the resolved token addresses, amounts, fees, and network fee estimate. See [`ExecuteSwapResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExecuteSwapResult) for the full type.

<Note>
  When using the `useSwap` hook, the `data` object is enriched with confirmation details: `receipt` for EOA transactions, and `transactionHash` / `receipts` / `userOperation` for Smart Accounts. These values are populated once the operation completes on-chain.
</Note>

### Token approvals

Swaps use [Permit2](https://github.com/Uniswap/permit2) for token transfers. The CDP Swap API signs the per-swap Permit2 permit automatically, but the `fromToken` must have an ERC-20 approval to the Permit2 contract.

<Note>
  Use `getSwapPrice` / `useGetSwapPrice` to check before executing — if `issues.allowance` is non-null, the taker needs to approve `issues.allowance.spender` (the Permit2 contract) for at least `fromAmount`. Approving a larger amount avoids re-approving on every swap.
</Note>

### Gas sponsorship

For Smart Account users, you can sponsor gas fees to enable gasless swaps. Pass `useCdpPaymaster: true` to use the [CDP Paymaster](/paymaster/introduction/welcome) on Base, or provide a custom `paymasterUrl` for any [ERC-7677](https://eips.ethereum.org/EIPS/eip-7677)-compatible paymaster. These options are ignored for EOA accounts.

<Warning>
  `useCdpPaymaster` is only supported on Base. For other chains, use `paymasterUrl`. You cannot specify both.
</Warning>

## Account selection

By default, the SDK auto-selects the taker account using the following heuristics:

| Configuration                  | Result                                                     |
| ------------------------------ | ---------------------------------------------------------- |
| 1 Smart Account + 1 EOA        | Prefers the Smart Account (EOA is typically just a signer) |
| 1 EOA only (no Smart Accounts) | Uses the EOA                                               |
| Multiple accounts              | Error: must specify `account`                              |

If auto-selection doesn't apply, pass `account` explicitly to choose which address to swap from.

## Supported networks

| Network  | Value      |
| -------- | ---------- |
| Base     | `base`     |
| Ethereum | `ethereum` |
| Arbitrum | `arbitrum` |
| Optimism | `optimism` |
| Polygon  | `polygon`  |

<Info>
  Swaps are currently supported on mainnet networks only; testnet support is not available. See [`EvmSwapsNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmSwapsNetwork) for the canonical list.
</Info>

## Error handling

Swap-specific failures throw a [`SwapError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/SwapError) with a typed `code` (see [`SwapErrorCode`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwapErrorCode) for all values). Input validation errors (invalid addresses, non-positive amounts, invalid slippage) throw an `InputValidationError` before any API call is made.

```typescript theme={null}
import { executeSwap, SwapError } from "@coinbase/cdp-core";

try {
  await executeSwap({ /* ... */ });
} catch (err) {
  if (err instanceof SwapError) {
    switch (err.code) {
      case "INSUFFICIENT_BALANCE":
        console.log("Not enough tokens to swap");
        break;
      case "INSUFFICIENT_LIQUIDITY":
        console.log("No route available — try a different pair or amount");
        break;
      default:
        console.log("Swap error:", err.message);
    }
  }
}
```

<Note>
  When using `useSwap`, check the returned `error` value instead of a `try/catch`. The same `instanceof SwapError` check applies.
</Note>

## FAQ

<AccordionGroup>
  <Accordion title="How do I specify token addresses?">
    Tokens are identified by their **0x-prefixed ERC-20 contract address** on the target network. The same token (e.g., USDC) has different addresses on different networks. You can find contract addresses on block explorers like [Basescan](https://basescan.org) or [Etherscan](https://etherscan.io).
  </Accordion>

  <Accordion title="What units should fromAmount be in?">
    `fromAmount` must be a **positive integer string in atomic units** (the smallest denomination of the token). For example, USDC has 6 decimals, so 1 USDC = `"1000000"`. WETH has 18 decimals, so 0.1 WETH = `"100000000000000000"`.
  </Accordion>

  <Accordion title="What does slippageBps control?">
    `slippageBps` sets the maximum acceptable price impact in basis points (1 bps = 0.01%). The default is `100` (1%), applied by the API when omitted. If the price moves beyond this threshold between the quote and execution, the transaction will revert to protect the user.
  </Accordion>

  <Accordion title="Are testnets supported?">
    Swaps are currently available on **mainnet networks only** (Base, Ethereum, Arbitrum, Optimism, Polygon). Testnet support is not yet available.
  </Accordion>

  <Accordion title="Can I swap the native gas token (ETH, POL)?">
    Yes. Use the sentinel address `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` as `fromToken` or `toToken` to represent the chain's native token (ETH on Ethereum/Base/Arbitrum/Optimism, POL on Polygon). No Permit2 approval is needed for native tokens.
  </Accordion>

  <Accordion title="Does the SDK handle token approvals?">
    The CDP Swap API handles the per-swap Permit2 signature automatically. However, the `fromToken` must have an ERC-20 approval to the Permit2 contract. See [Token approvals](#token-approvals) for details.
  </Accordion>

  <Accordion title="What's the difference between useSwap and executeSwap?">
    `executeSwap` (core) returns a `Promise` that resolves with the swap result (transaction hash or user op hash) as soon as it's submitted. `useSwap` (hooks) additionally tracks on-chain confirmation — `status` stays `"pending"` until the transaction receipt (EOA) or user operation (Smart Account) is confirmed, then moves to `"success"`.
  </Accordion>
</AccordionGroup>

## Full example

<CodeGroup>
  ```tsx [expandable] React hooks theme={null}
  import { useSwap, useGetSwapPrice } from "@coinbase/cdp-hooks";
  import { SwapError } from "@coinbase/cdp-core";
  import { useId, useState } from "react";

  function SwapComponent() {
    const inputId = useId();
    const [fromAmount, setFromAmount] = useState("1000000");

    const swapParams = {
      network: "base" as const,
      fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" as const, // USDC
      toToken: "0x4200000000000000000000000000000000000006" as const,   // WETH
      fromAmount,
    };

    const { data: price, status: priceStatus, error: priceError } = useGetSwapPrice(swapParams);

    const { swap, data, status: swapStatus, error: swapError } = useSwap();

    const hasIssues = price?.liquidityAvailable && (price.issues?.balance || price.issues?.allowance);
    const canSwap = price?.liquidityAvailable && !hasIssues && swapStatus !== "pending";

    const handleSwap = async () => {
      await swap(swapParams);
    };

    return (
      <div>
        <label htmlFor={inputId}>Amount in atomic units</label>
        <input
          id={inputId}
          value={fromAmount}
          onChange={(e) => setFromAmount(e.target.value)}
        />

        {priceStatus === "pending" && <p>Loading price...</p>}
        {priceError && <p>Price error: {priceError.message}</p>}

        {price?.liquidityAvailable && (
          <div>
            <p>Expected output: {price.toAmount}</p>
            <p>Minimum after slippage: {price.minToAmount}</p>
            {price.totalNetworkFee && <p>Network fee: {price.totalNetworkFee}</p>}
            {price.fees?.protocolFee && (
              <p>Protocol fee: {price.fees.protocolFee.amount}</p>
            )}
            {price.issues?.balance && <p>Insufficient balance</p>}
            {price.issues?.allowance && <p>Token allowance required</p>}
          </div>
        )}

        {price && !price.liquidityAvailable && (
          <p>No liquidity available for this pair</p>
        )}

        <button onClick={handleSwap} disabled={!canSwap}>
          {swapStatus === "pending" ? "Swapping..." : "Swap"}
        </button>

        {swapStatus === "pending" && data && (
          <p>
            Submitted:{" "}
            {data.type === "evm-eoa" ? data.transactionHash : data.userOpHash}
          </p>
        )}

        {swapStatus === "success" && data && (
          <p>Swap confirmed! Received: {data.toAmount}</p>
        )}

        {swapError instanceof SwapError && (
          <p>Swap failed ({swapError.code}): {swapError.message}</p>
        )}
        {swapError && !(swapError instanceof SwapError) && (
          <p>Unexpected error: {swapError.message}</p>
        )}
      </div>
    );
  }
  ```

  ```typescript [expandable] Vanilla JS theme={null}
  import { getSwapPrice, executeSwap, SwapError } from "@coinbase/cdp-core";

  const params = {
    network: "base" as const,
    fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC
    toToken: "0x4200000000000000000000000000000000000006",   // WETH
    fromAmount: "1000000", // 1 USDC (6 decimals)
  };

  // Step 1: Get a price estimate (e.g., when the user picks a token pair)
  try {
    const price = await getSwapPrice(params);

    if (!price.liquidityAvailable) {
      // No route exists — show a message and let the user adjust
      return;
    }

    console.log("Expected output:", price.toAmount);
    console.log("Minimum after slippage:", price.minToAmount);
    console.log("Network fee:", price.totalNetworkFee);

    if (price.fees?.protocolFee) {
      console.log("Protocol fee:", price.fees.protocolFee.amount, price.fees.protocolFee.token);
    }

    if (price.issues?.balance) {
      console.warn("Insufficient balance");
    }

    if (price.issues?.allowance) {
      console.warn("Token allowance required for", price.issues.allowance.spender);
    }
  } catch (err) {
    console.error("Failed to fetch price:", err);
  }

  // Step 2: Execute the swap (e.g., after the user confirms)
  try {
    const result = await executeSwap(params);

    if (result.type === "evm-eoa") {
      console.log("Transaction hash:", result.transactionHash);
    } else {
      console.log("User operation hash:", result.userOpHash);
    }

    console.log("Sold:", result.fromAmount, result.fromToken);
    console.log("Expected:", result.toAmount, result.toToken);
    console.log("Minimum:", result.minToAmount);
    console.log("Network fee:", result.totalNetworkFee);
  } catch (err) {
    if (err instanceof SwapError) {
      console.error(`Swap failed [${err.code}]:`, err.message);
    } else {
      console.error("Unexpected error:", err);
    }
  }
  ```
</CodeGroup>

## Reference

### `@coinbase/cdp-core`

| Resource                                                                                                    | Description                                |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| [`getSwapPrice`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getSwapPrice)                      | Get an indicative price                    |
| [`executeSwap`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/executeSwap)                        | Execute a swap                             |
| [`GetSwapPriceOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetSwapPriceOptions)     | Parameters for price requests              |
| [`GetSwapPriceResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetSwapPriceResult)       | Price response when liquidity is available |
| [`SwapUnavailableResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwapUnavailableResult) | Price response when no route exists        |
| [`ExecuteSwapOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExecuteSwapOptions)       | Parameters for swap execution              |
| [`ExecuteSwapResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExecuteSwapResult)         | Swap result type (EOA / Smart Account)     |
| [`SwapError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/SwapError)                              | Typed error class for swap failures        |

### `@coinbase/cdp-hooks`

| Resource                                                                                                             | Description                            |
| -------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| [`useGetSwapPrice`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useGetSwapPrice)                        | Reactive price fetching                |
| [`useSwap`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSwap)                                        | Execute and track a swap               |
| [`UseGetSwapPriceOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/UseGetSwapPriceOptions)         | Options for `useGetSwapPrice`          |
| [`UseGetSwapPriceReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseGetSwapPriceReturnType) | Return type of `useGetSwapPrice`       |
| [`UseSwapReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseSwapReturnType)                 | Return type of `useSwap`               |
| [`SwapTransactionData`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SwapTransactionData)             | Hook swap result (EOA / Smart Account) |

## What to read next

<CardGroup>
  <Card title="USDC Send" icon="paper-plane" href="/embedded-wallets/usdc-send-hooks">
    Send USDC with a simple, unified API across all account types
  </Card>

  <Card title="Smart Accounts" icon="wallet" href="/embedded-wallets/evm-features/smart-accounts">
    Learn about EVM Smart Accounts and gas abstraction
  </Card>

  <Card title="React Hooks Reference" icon="code" href="/embedded-wallets/react-hooks">
    Explore all available React hooks for embedded wallets
  </Card>

  <Card title="Trade API" icon="chart-line" href="/trade-api/welcome">
    Onchain swaps for trading bots, DeFi apps, and server-side integrations
  </Card>
</CardGroup>

