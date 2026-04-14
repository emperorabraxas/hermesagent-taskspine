# Batching Instructions
Source: https://docs.cdp.coinbase.com/server-wallets/v2/solana-features/batching-instructions



## Overview

A Solana transaction is a list of instructions that are executed in order. This allows developers to batch multiple instructions into a single transaction, reducing the number of transactions required to complete a complex multi-step process.

## Prerequisites

It is assumed you have already completed the [Quickstart](/server-wallets/v2/introduction/quickstart) guide.

## Create and send transaction with multiple instructions

In this example, we will:

* Create a Solana account
* Construct multiple instructions to be executed in the transaction
* Sign the transaction with the Solana account
* Send the transaction to the Solana network

<CodeGroup>
  ```ts main.ts lines wrap [expandable] theme={null}
  import {
    Connection,
    PublicKey,
    SystemProgram,
    Transaction,
  } from "@solana/web3.js";
  import { CdpClient } from "@coinbase/cdp-sdk";
  import dotenv from "dotenv";

  dotenv.config();

  const cdp = new CdpClient();

  const connection = new Connection("https://api.devnet.solana.com");

  async function createAccount() {
    const account = await cdp.solana.createAccount();
    console.log(`Created account: ${account.address}`);
    return account;
  }

  async function requestFaucet(address: string) {
    await cdp.solana.requestFaucet({
      address,
      token: "sol",
    });
  }

  async function waitForBalance(address: string) {
    let balance = 0;
    let attempts = 0;
    const maxAttempts = 30;

    while (balance === 0 && attempts < maxAttempts) {
      balance = await connection.getBalance(new PublicKey(address));
      if (balance === 0) {
        console.log("Waiting for funds...");
        await new Promise(resolve => setTimeout(resolve, 1000));
        attempts++;
      } else {
        console.log("Account funded with", balance / 1e9, "SOL");
      }
    }

    if (balance === 0) {
      throw new Error("Account not funded after multiple attempts");
    }
  }

  async function sendTransaction(address: string) {
    // Amount of lamports to send (default: 1000 = 0.000001 SOL)
    const lamportsToSend = 1000;
    const fromAddress = new PublicKey(address)
    const destinations = [
      "ANVUJaJoVaJZELtV2AvRp7V5qPV1B84o29zAwDhPj1c2",
      "EeVPcnRE1mhcY85wAh3uPJG1uFiTNya9dCJjNUPABXzo",
      "4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK",
    ]

    const { blockhash } = await connection.getLatestBlockhash();

    // Create instructions for each destination
    const instructions = destinations.map((toAddress) => {
      return SystemProgram.transfer({
        fromPubkey: fromAddress,
        toPubkey: new PublicKey(toAddress),
        lamports: lamportsToSend,
      })
    })

    // Create a single transaction with all instructions
    const transaction = new Transaction();
    transaction.add(...instructions);

    transaction.recentBlockhash = blockhash;
    transaction.feePayer = fromAddress;

    const serializedTx = Buffer.from(
      transaction.serialize({ requireAllSignatures: false })
    ).toString("base64");

    const { signature: txSignature } = await cdp.solana.signTransaction({
      address,
      transaction: serializedTx,
    });
    const decodedSignedTx = Buffer.from(txSignature, "base64");

    console.log("Sending transaction...");
    const txSendSignature = await connection.sendRawTransaction(decodedSignedTx);

    const latestBlockhash = await connection.getLatestBlockhash();

    console.log("Waiting for transaction to be confirmed...");
    const confirmation = await connection.confirmTransaction({
      signature: txSendSignature,
      blockhash: latestBlockhash.blockhash,
      lastValidBlockHeight: latestBlockhash.lastValidBlockHeight,
    });

    if (confirmation.value.err) {
      throw new Error(`Transaction failed: ${confirmation.value.err.toString()}`);
    }

    console.log(`Sent SOL: https://explorer.solana.com/tx/${txSendSignature}?cluster=devnet`);
  }

  async function main() {
    const account = await createAccount();
    await requestFaucet(account.address);
    await waitForBalance(account.address);
    await sendTransaction(account.address);
  }

  main().catch(console.error)
  ```

  ```python main.py lines wrap [expandable] theme={null}
  import time
  import base64
  import asyncio
  from cdp import CdpClient
  from dotenv import load_dotenv
  from solana.rpc.api import Client as SolanaClient
  from solana.rpc.types import TxOpts
  from solders.pubkey import Pubkey as PublicKey
  from solders.system_program import TransferParams, transfer
  from solders.message import Message

  load_dotenv()

  cdp = CdpClient()

  connection = SolanaClient("https://api.devnet.solana.com")

  async def create_sol_account():
      account = await cdp.solana.create_account()
      print(f"Created account: {account.address}")
      return account


  async def request_faucet(address: str):
      await cdp.solana.request_faucet(
          address,
          token="sol"
      )


  async def wait_for_balance(address: str):
      balance = 0
      max_attempts = 30
      attempts = 0

      while balance == 0 and attempts < max_attempts:
          balance_resp = connection.get_balance(PublicKey.from_string(address))
          balance = balance_resp.value
          if balance == 0:
              print("Waiting for funds...")
              time.sleep(1)
              attempts += 1
          else:
              print(f"Account funded with {balance / 1e9} SOL ({balance} lamports)")

      if balance == 0:
          raise ValueError("Account not funded after multiple attempts")


  async def send_transaction(address: str):
      # Amount of lamports to send (default: 1000 = 0.000001 SOL)
      lamports_to_send = 1000;
      from_address = PublicKey.from_string(address)

      # Multiple destinations in one transaction
      destinations = [
          PublicKey.from_string("ANVUJaJoVaJZELtV2AvRp7V5qPV1B84o29zAwDhPj1c2"),
          PublicKey.from_string("EeVPcnRE1mhcY85wAh3uPJG1uFiTNya9dCJjNUPABXzo"),
          PublicKey.from_string("4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK"),
      ]

      blockhash_resp = connection.get_latest_blockhash()
      blockhash = blockhash_resp.value.blockhash

      # Create a transfer instruction for each destination
      transfer_instructions = [
          transfer(
              TransferParams(
                  from_pubkey=from_address,
                  to_pubkey=destination,
                  lamports=lamports_to_send,
              )
          ) for destination in destinations
      ]

      message = Message.new_with_blockhash(
          transfer_instructions,
          from_address,
          blockhash,
      )

      # Create a transaction envelope with signature space
      sig_count = bytes([1])  # 1 byte for signature count (1)
      empty_sig = bytes([0] * 64)  # 64 bytes of zeros for the empty signature
      message_bytes = bytes(message)  # Get the serialized message bytes

      # Concatenate to form the transaction bytes
      tx_bytes = sig_count + empty_sig + message_bytes

      # Encode to base64 used by CDP API
      serialized_tx = base64.b64encode(tx_bytes).decode("utf-8")

      signed_tx_response = await cdp.solana.sign_transaction(
          address,
          transaction=serialized_tx,
      )

      # Decode the signed transaction from base64
      decoded_signed_tx = base64.b64decode(signed_tx_response.signed_transaction)

      print("Sending transaction...")
      tx_resp = connection.send_raw_transaction(
          decoded_signed_tx,
          opts=TxOpts(skip_preflight=False, preflight_commitment="processed"),
      )
      signature = tx_resp.value

      print("Waiting for transaction to be confirmed...")
      confirmation = connection.confirm_transaction(signature, commitment="processed")

      if hasattr(confirmation, "err") and confirmation.err:
          raise ValueError(f"Transaction failed: {confirmation.err}")

      print(f"Sent SOL: https://explorer.solana.com/tx/{signature}?cluster=devnet")


  async def main():
      account = await create_sol_account()
      await request_faucet(account.address)
      await wait_for_balance(account.address)
      await send_transaction(account.address)

      await cdp.close()

  asyncio.run(main())
  ```
</CodeGroup>

After running the above snippet, you should see output similar to the following:

```
Created account: Af8cVHK2DZXcT4WhK6VDZ3h2zFxbEfgamsRkrB7dUcfF
Waiting for funds...
Account funded with 0.00125 SOL (1250000 lamports)
Sending transaction...
Waiting for transaction to be confirmed...
Sent SOL: https://explorer.solana.com/tx/56oRrY2nHSbncysmrW6vtBaUoyvWnRrMqN1joGNzaY3TNmPSTM653skDjbj2jDEdMA4QqFo9c4GY4hTnRhScgJk5?cluster=devnet
```

## What to read next

* [v2 API Reference documentation](/api-reference/v2/authentication): Learn how to use Wallet Secrets to authenticate requests to the v2 Server Wallet.
* [Sponsor Solana Transactions](/server-wallets/v2/solana-features/sponsor-transactions): Learn how to sponsor gas on Solana transactions.

