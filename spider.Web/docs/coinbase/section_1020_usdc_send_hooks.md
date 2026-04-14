# USDC Send Hooks
Source: https://docs.cdp.coinbase.com/embedded-wallets/usdc-send-hooks



<Tags />

## Overview

Send USDC with a simple, unified API that works across all account types and networks. The `useSendUsdc` hook automatically detects whether you're using Solana, EVM Smart Accounts, or EVM EOAs, handling all protocol-specific complexity for you.

**Making USDC transfers as simple as specifying a recipient, amount, and network.**

<Info>
  This hook works with **all account types**: Solana accounts, EVM Smart Accounts, and EVM EOAs (Externally Owned Accounts). It automatically detects which type you're using and routes the transaction accordingly.
</Info>

## Why use the USDC Send Hook?

Traditional USDC transfers require managing significant protocol-specific complexity:

* **Contract addresses** - Different USDC contracts on each network
* **Decimal conversion** - Converting human-readable amounts to 6-decimal atomic units
* **ERC-20 encoding** - Manually encoding transfer function calls (EVM)
* **Associated Token Accounts** - Creating and managing Associated Token Accounts (Solana)
* **Gas sponsorship** - Configuring Paymasters and User Operations (EVM Smart Accounts)
* **Account type detection** - Determining if an address is EOA, Smart Account, or Solana

The USDC Send Hook eliminates all of this complexity:

```tsx theme={null}
await sendUsdc({
  to: "0xRecipient...", // EVM or Solana Address
  amount: "25.50",
  network: "base",
});
```

## Key Features

<CardGroup>
  <Card title="Simple API" icon="sparkles">
    Just three parameters: `to`, `amount`, and `network` — that's it
  </Card>

  <Card title="Cross-Chain" icon="link">
    Works across Solana and EVM networks with the same hook
  </Card>

  <Card title="Universal Accounts" icon="users">
    Supports EOAs and Smart Accounts — automatically detects which you're using
  </Card>

  <Card title="Gas Sponsorship" icon="gas-pump">
    Built-in Paymaster support for gasless Smart Account transactions
  </Card>
</CardGroup>

## useSendUsdc

A single hook that sends USDC across all supported account types and networks.

### Basic Usage

```tsx theme={null}
import { useSendUsdc } from "@coinbase/cdp-hooks";

function SendUsdcComponent() {
  const { sendUsdc, data, error, status } = useSendUsdc();

  const handleSend = async () => {
    try {
      // Three required fields: to, amount, network
      // Automatically selects sender using smart heuristics
      const result = await sendUsdc({
        to: "0x1234567890123456789012345678901234567890",
        amount: "25.50",
        network: "base-sepolia",
      });

      if (result.type === "evm-eoa") {
        console.log("EOA Transaction:", result.transactionHash);
      } else if (result.type === "evm-smart") {
        console.log("Smart Account UserOp:", result.userOpHash);
      } else if (result.type === "solana") {
        console.log("Solana Transaction:", result.transactionSignature);
      }
    } catch (err) {
      console.error("Failed to send USDC:", err);
    }
  };

  return (
    <div>
      <button onClick={handleSend} disabled={status === "pending"}>
        {status === "pending" ? "Sending..." : "Send 25.50 USDC"}
      </button>

      {status === "success" && data && (
        <p>✅ USDC sent successfully!</p>
      )}

      {error && (
        <p>❌ Error: {error.message}</p>
      )}
    </div>
  );
}
```

### Explicit Account Selection

If auto-selection doesn't apply (e.g., you have multiple accounts), explicitly specify which account to send from:

```tsx theme={null}
import { useSendUsdc, useCurrentUser } from "@coinbase/cdp-hooks";

function SendFromSpecificAccount() {
  const { currentUser } = useCurrentUser();
  const { sendUsdc, status } = useSendUsdc();

  const handleSend = async () => {
    // Select specific account to send from
    const smartAccount = currentUser?.evmSmartAccountObjects?.[0]?.address;

    await sendUsdc({
      from: smartAccount, // Explicitly specify sender
      to: "0x1234567890123456789012345678901234567890",
      amount: "10.00",
      network: "base",
      useCdpPaymaster: true, // Optional: for Smart Accounts
    });
  };

  return <button onClick={handleSend}>Send from Smart Account</button>;
}
```

### Advanced Options

```tsx theme={null}
import { useSendUsdc } from "@coinbase/cdp-hooks";

function AdvancedSendUsdc() {
  const { sendUsdc } = useSendUsdc();

  const handleEvmSend = async () => {
    await sendUsdc({
      to: "0x1234567890123456789012345678901234567890",
      amount: "50.00",
      network: "base",
      useCdpPaymaster: false,
      paymasterUrl: "https://custom-paymaster.com", // Custom Paymaster
    });
  };

  const handleSolanaSend = async () => {
    await sendUsdc({
      to: "ExXhNkgYf6efh7YyqDRVxPZuzafobao1A74drUdp8trd",
      amount: "10.00",
      network: "solana",
      createRecipientAta: true, // Create recipient ATA (Solana only)
    });
  };

  return (
    <div>
      <button onClick={handleEvmSend}>Send with Advanced Options</button>
      <button onClick={handleSolanaSend}>Send with Advanced Options</button>
    </div>
  );
}
```

## Parameters

| Parameter            | Type                          | Required | Description                                                           |
| -------------------- | ----------------------------- | -------- | --------------------------------------------------------------------- |
| `to`                 | `EvmAddress \| SolanaAddress` | Yes      | The recipient address (EVM or Solana format)                          |
| `amount`             | `string`                      | Yes      | Human-readable USDC amount (e.g., `"1.50"` for 1.5 USDC)              |
| `network`            | `SendUsdcNetwork`             | Yes      | Network to send on (EVM or Solana network)                            |
| `from`               | `EvmAddress \| SolanaAddress` | No       | Sender address (auto-selected using smart heuristics if not provided) |
| `useCdpPaymaster`    | `boolean`                     | No       | Use CDP Paymaster for gas sponsorship (EVM Smart Accounts only)       |
| `paymasterUrl`       | `string`                      | No       | Custom Paymaster URL (EVM Smart Accounts only)                        |
| `createRecipientAta` | `boolean`                     | No       | Auto-create recipient's ATA (Solana only, default: `false`)           |

### Auto-Selection Logic

The hook automatically selects the `from` address when:

* You have **exactly one** account (Solana, Smart Account, or EOA)

**Single Chain: EVM Only**

| Configuration                  | Result                                                   |
| ------------------------------ | -------------------------------------------------------- |
| 1 Smart Account + 1 EOA        | ✅ Prefers Smart Account (EOA is typically just a signer) |
| 1 EOA only (no Smart Accounts) | ✅ Uses the EOA                                           |
| Any other EVM configuration    | ❌ Error - must specify `from`                            |

**Single Chain: Solana Only**

| Configuration            | Result                        |
| ------------------------ | ----------------------------- |
| 1 Solana account         | ✅ Uses that account           |
| Multiple Solana accounts | ❌ Error - must specify `from` |

**Cross-Chain: EVM + Solana**

| Configuration                | Result                                           |
| ---------------------------- | ------------------------------------------------ |
| Both EVM and Solana accounts | ❌ Error - must specify `from` to avoid ambiguity |

## Supported Networks

### EVM Networks

* `base` - Base Mainnet
* `base-sepolia` - Base Sepolia Testnet
* `ethereum` - Ethereum Mainnet
* `ethereum-sepolia` - Ethereum Sepolia Testnet
* `avalanche` - Avalanche C-Chain
* `polygon` - Polygon Mainnet
* `optimism` - Optimism Mainnet
* `arbitrum` - Arbitrum Mainnet

### Solana Networks

* `solana` - Solana Mainnet Beta
* `solana-devnet` - Solana Devnet

<Note>
  The hook automatically waits for transaction confirmation:

  * **EOA**: Waits for `TransactionReceipt`
  * **Smart Account**: Waits for User Operation completion
  * **Solana**: Returns immediately with signature
</Note>

<Tip>
  By default, `createRecipientAta` is `false` to avoid unexpected costs. If the recipient doesn't have a USDC token account and you don't set this to `true`, the transaction will fail with a clear error message.
</Tip>

## FAQ

<AccordionGroup>
  <Accordion title="What happens if I have both EVM and Solana accounts?">
    You'll receive an error: **"Multiple account types detected (EVM and Solana). Please specify 'from' address..."**. This prevents cross-chain ambiguity—you must explicitly choose which account to send from.
  </Accordion>

  <Accordion title="What USDC decimals are used?">
    USDC uses **6 decimals** on all supported chains (both EVM and Solana). The hook handles this conversion automatically, so you can use human-readable amounts like `"1.50"`.
  </Accordion>

  <Accordion title="What's the cost of createRecipientAta on Solana?">
    Setting `createRecipientAta: true` will create the recipient's USDC token account if it doesn't exist. This costs approximately **\~0.002 SOL** for rent exemption, which the **sender pays**. This is why it defaults to `false`—to avoid unexpected costs.
  </Accordion>

  <Accordion title="Can I customize the Paymaster for gas sponsorship with EVM Smart Accounts?">
    Yes! Use the `paymasterUrl` parameter for Smart Accounts:

    ```tsx theme={null}
    await sendUsdc({
      to: recipient,
      amount: "10.00",
      network: "base",
      useCdpPaymaster: false,
      paymasterUrl: "https://my-paymaster.example.com",
    });
    ```
  </Accordion>
</AccordionGroup>

## What to read next

<CardGroup>
  <Card title="Smart Accounts" icon="wallet" href="/embedded-wallets/evm-features/smart-accounts">
    Learn about EVM Smart Accounts and gas abstraction
  </Card>

  <Card title="React Hooks Reference" icon="code" href="/embedded-wallets/react-hooks">
    Explore all available React hooks for embedded wallets
  </Card>

  <Card title="Solana Transactions" icon="paper-plane" href="/embedded-wallets/solana-features/sending-transactions">
    Deep dive into Solana transaction handling
  </Card>

  <Card title="Quickstart" icon="rocket" href="/embedded-wallets/quickstart">
    Get started with embedded wallets in your React app
  </Card>
</CardGroup>

