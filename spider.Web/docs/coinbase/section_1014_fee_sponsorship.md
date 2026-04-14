# Fee Sponsorship
Source: https://docs.cdp.coinbase.com/embedded-wallets/solana-features/fee-sponsorship



## Overview

Fee sponsorship lets CDP pay the Solana network fee on behalf of your users.
Users can send transactions without holding SOL in their wallet to cover gas.

This feature is in private preview and available to enterprise-scale integrations only.
To opt in, [apply for access](https://docs.google.com/forms/d/e/1FAIpQLSdMG0DDGkLDV73H1QNVQ50hrjVRBtNgfBPwVVW_f8RAASoWgQ/viewform).
Once approved, pass `useCdpSponsor: true` to `useSendSolanaTransaction` or `useSendSolanaUsdc`.

## Sponsoring a SOL transfer

Use `useSendSolanaTransaction` with `useCdpSponsor: true`. CDP signs the transaction as the fee payer, so users don't need SOL for the network fee.

```tsx sendSolanaTransactionSponsored.tsx theme={null}
import { useSendSolanaTransaction, useSolanaAddress } from "@coinbase/cdp-hooks";
import { PublicKey, Transaction, SystemProgram, SYSVAR_RECENT_BLOCKHASHES_PUBKEY } from "@solana/web3.js";
import { Buffer } from "buffer";

function createAndEncodeTransaction(fromAddress: string, toAddress: string, lamports: number) {
  const fromPubkey = new PublicKey(fromAddress);
  const toPubkey = new PublicKey(toAddress);

  const transaction = new Transaction().add(
    SystemProgram.transfer({ fromPubkey, toPubkey, lamports }),
  );

  transaction.recentBlockhash = SYSVAR_RECENT_BLOCKHASHES_PUBKEY.toBase58();
  transaction.feePayer = fromPubkey;

  return Buffer.from(transaction.serialize({ requireAllSignatures: false })).toString("base64");
}

function SendSponsoredTransaction() {
  const { sendSolanaTransaction } = useSendSolanaTransaction();
  const { solanaAddress } = useSolanaAddress();

  const handleSend = async () => {
    if (!solanaAddress) return;

    const transaction = createAndEncodeTransaction(
      solanaAddress,
      "recipient-address",
      1_000_000, // 0.001 SOL
    );

    const result = await sendSolanaTransaction({
      solanaAccount: solanaAddress,
      network: "solana-mainnet",
      transaction,
      useCdpSponsor: true,
    });

    console.log("Transaction signature:", result.transactionSignature);
  };

  return <button onClick={handleSend}>Send Transaction</button>;
}
```

## Sponsoring a USDC transfer

Use `useSendSolanaUsdc` with `useCdpSponsor: true`. When `createRecipientAta` is also enabled, CDP sponsors both the network fee and the associated token account (ATA) rent for the recipient.

```tsx sendSolanaUsdcSponsored.tsx theme={null}
import { useSendSolanaUsdc, useSolanaAddress } from "@coinbase/cdp-hooks";

function SendSponsoredUsdc() {
  const { sendSolanaUsdc } = useSendSolanaUsdc();
  const { solanaAddress } = useSolanaAddress();

  const handleSend = async () => {
    if (!solanaAddress) return;

    const result = await sendSolanaUsdc({
      solanaAccount: solanaAddress,
      to: "recipient-address",
      amount: "1.50",
      network: "solana-mainnet",
      createRecipientAta: true,
      useCdpSponsor: true,
    });

    console.log("Transaction signature:", result.transactionSignature);
  };

  return <button onClick={handleSend}>Send USDC</button>;
}
```

## Rate limits

CDP enforces sponsorship limits. If a limit is exceeded, the API returns a `429` response. To request a limit increase, reach out in the [Coinbase Developer Discord](https://discord.gg/cdp).

## What to read next

* **[Sending Transactions](/embedded-wallets/solana-features/sending-transactions)**: Build and send Solana transactions without fee sponsorship
* **[Signing](/embedded-wallets/solana-features/signing)**: Sign Solana messages and transactions without broadcasting
* **[React Hooks](/embedded-wallets/react-hooks)**: Explore all available CDP hooks for embedded wallets

