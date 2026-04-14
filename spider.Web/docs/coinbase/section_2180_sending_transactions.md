# Sending Transactions
Source: https://docs.cdp.coinbase.com/server-wallets/v2/solana-features/sending-transactions



## Overview

This guide covers the fundamentals of sending transactions on Solana using the CDP v2 Server Wallet. You will learn how to construct transactions and submit them to the Solana network.

Solana transactions benefit from a single API that supports signing and broadcasting. With CDP, signing keys are securely managed in the platform's infrastructure.

1. **Create transaction**: Build a transaction with one or more instructions
2. **Send transaction**: Use CDP to send the serialized transaction
3. **Confirm transaction**: Wait for network confirmation

## Prerequisites

It is assumed you have:

* Completed the [Quickstart](/server-wallets/v2/introduction/quickstart) guide
* Basic understanding of [Solana accounts](/server-wallets/v2/introduction/accounts#solana-accounts)
* Installed dependencies:
  * For TypeScript: `@solana/web3.js`, `@coinbase/cdp-sdk`, and `dotenv`
  * For Python: `solana`, `solders`, `cdp-sdk`, and `python-dotenv`

<Note>
  The following steps break down the transaction flow into digestible pieces. If you prefer to see the full working code immediately, skip to the [Complete example](#complete-example) section below.
</Note>

## 1. Create a Solana account

First, create or retrieve a Solana account using CDP. The below example uses `solana-devnet` and will source `SOL` from CDP faucet to transfer.

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import "dotenv/config";

  const cdp = new CdpClient();

  const account = await cdp.solana.createAccount({
    name: "test-sol-account",
  });

  let fromAddress: string;
  fromAddress = account.address;
  console.log("Successfully created new SOL account:", fromAddress);

  // Request SOL from faucet
  const faucetResp = await cdp.solana.requestFaucet({
    address: fromAddress,
    token: "sol",
  });
  console.log(
    "Successfully requested SOL from faucet:",
    faucetResp.signature
  );
  ```

  ```python Python theme={null}
  from cdp import CdpClient
  import asyncio

  async def create_and_fund_account():
      async with CdpClient() as cdp:
          # Create account
          print("Creating account...")
          account = await cdp.solana.create_account()
          sender_address = account.address
          print(f"Successfully created account: {sender_address}")
          
          # Request SOL from faucet
          print(f"Requesting SOL from faucet for {sender_address}...")
          response = await cdp.solana.request_faucet(address=sender_address, token="sol")
          transaction_signature = response.transaction_signature
          print(f"Successfully requested SOL from faucet: {transaction_signature}")
          
          return sender_address

  # Run the async function
  sender_address = asyncio.run(create_and_fund_account())
  ```
</CodeGroup>

## 2. Build the transaction

Prepare a transaction with one or more instructions.
The transaction may contain several instructions, each of which may require signatures from different account keys.
Here is a simple SOL transfer.

<Note>
  We set the blockhash to a static value temporarily since the CDP v2 Server Wallet will update it before it is sent to the network.
</Note>

<CodeGroup>
  ```typescript TypeScript theme={null}
  import {
    PublicKey,
    SystemProgram,
    SYSVAR_RECENT_BLOCKHASHES_PUBKEY,
    Transaction,
  } from "@solana/web3.js";

  // Required: Destination address to send SOL to (replace with your recipient)
  const destinationAddress = "3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE";

  // Amount of lamports to send (default: 1000 = 0.000001 SOL)
  const lamportsToSend = 1000;

  // Assumes fromAddress is defined from step 1
  let fromAddress: string; // Your Solana account address

  const transaction = new Transaction();
  transaction.add(
    SystemProgram.transfer({
      fromPubkey: new PublicKey(fromAddress),
      toPubkey: new PublicKey(destinationAddress),
      lamports: lamportsToSend,
    })
  );
  transaction.recentBlockhash = SYSVAR_RECENT_BLOCKHASHES_PUBKEY.toBase58();
  transaction.feePayer = new PublicKey(fromAddress);
  ```

  ```python Python theme={null}
  from solana.rpc.api import Client as SolanaClient
  from solders.pubkey import Pubkey as PublicKey
  from solders.system_program import TransferParams, transfer
  from solders.message import Message

  # Required: Destination address to send SOL to (replace with your recipient)
  destination_address = "3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE"

  # Amount of lamports to send (default: 1000 = 0.000001 SOL)
  amount = 1000

  # Assumes sender_address is defined from step 1
  sender_address = "YOUR_SENDER_ADDRESS"  # Your Solana account address

  # Build transfer instruction
  source_pubkey = PublicKey.from_string(sender_address)
  dest_pubkey = PublicKey.from_string(destination_address)

  transfer_params = TransferParams(
      from_pubkey=source_pubkey, to_pubkey=dest_pubkey, lamports=amount
  )
  transfer_instr = transfer(transfer_params)

  # Create message with the transfer instruction
  message = Message.new_with_blockhash(
      [transfer_instr],
      source_pubkey,
      Hash.from_string("SysvarRecentB1ockHashes11111111111111111111"),
  )
  ```
</CodeGroup>

## 3. Serialize transaction

Serialize the transaction for signing:

<CodeGroup>
  ```typescript TypeScript theme={null}
  const serializedTx = Buffer.from(
    transaction.serialize({ requireAllSignatures: false })
  ).toString("base64");

  console.log("Transaction serialized successfully");
  ```

  ```python Python theme={null}
  import base64

  # Create a transaction envelope with signature space
  sig_count = bytes([1])  # 1 byte for signature count (1)
  empty_sig = bytes([0] * 64)  # 64 bytes of zeros for the empty signature
  message_bytes = bytes(message)  # Get the serialized message bytes

  # Concatenate to form the transaction bytes
  tx_bytes = sig_count + empty_sig + message_bytes

  # Encode to base64 used by CDP API
  serialized_tx = base64.b64encode(tx_bytes).decode("utf-8")

  print("Transaction serialized successfully")
  ```
</CodeGroup>

## 4. Send the transaction

Use CDP to send the serialized transaction:

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";

  // Assumes cdp client is initialized from step 1
  const cdp = new CdpClient();

  const txResult = await cdp.solana.sendTransaction({
      network: "solana-devnet",
      transaction: serializedTx,
  });

  const signature = txResult.signature;
  console.log("Solana transaction hash:", signature);
  ```

  ```python Python theme={null}
  from cdp import CdpClient
  import base64

  async def send_transaction(sender_address: str, serialized_tx: str):
      async with CdpClient() as cdp:
              print("Sending transaction to network...")
              tx_resp = await cdp.solana.send_transaction(
                  network="solana-devnet",
                  transaction=serialized_tx,
              )
              signature = tx_resp.transaction_signature
              print(f"Solana transaction hash: {signature}")
              return signature

  # Send the transaction
  import asyncio
  tx_result = asyncio.run(send_transaction(sender_address, serialized_tx))
  ```
</CodeGroup>

## 5. Confirm

Wait for confirmation after you submitted the transaction to the network.

<CodeGroup>
  ```typescript TypeScript theme={null}
  console.log("Waiting for transaction to be confirmed");
  const latestBlockhash = await connection.getLatestBlockhash();
  const confirmation = await connection.confirmTransaction({
    signature,
    blockhash: latestBlockhash.blockhash,
    lastValidBlockHeight: latestBlockhash.lastValidBlockHeight,
  });

  if (confirmation.value.err) {
    throw new Error(
      `Transaction failed: ${confirmation.value.err.toString()}`
    );
  }

  console.log(
    "Transaction confirmed:",
    confirmation.value.err ? "failed" : "success"
  );
  console.log(
    `Transaction explorer link: https://explorer.solana.com/tx/${signature}?cluster=devnet`
  );
  ```

  ```python Python theme={null}
  print("Confirming transaction...")
  confirmation = connection.confirm_transaction(signature, commitment="processed")

  if hasattr(confirmation, "err") and confirmation.err:
      raise ValueError(f"Transaction failed: {confirmation.err}")

  print(
      f"Transaction confirmed: {'failed' if hasattr(confirmation, 'err') and confirmation.err else 'success'}"
  )
  print(
      f"Transaction explorer link: https://explorer.solana.com/tx/{signature}?cluster=devnet"
  )
  ```
</CodeGroup>

## Complete example

<Accordion title="View complete runnable examples">
  Here's the complete, runnable example for easy copy and paste:

  <CodeGroup>
    ```typescript TypeScript theme={null}
    // Usage: pnpm tsx solana/sendTransaction.ts [sourceAddress]

    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    import {
        Connection,
        PublicKey,
        SystemProgram,
        SYSVAR_RECENT_BLOCKHASHES_PUBKEY,
        Transaction,
    } from "@solana/web3.js";

    /**
     * This script will:
     * 1. Either use a provided Solana address or create a new one
     * 2. If a new account is created, requests SOL from CDP faucet
     * 3. Creates and sends a transaction with CDP to send SOL to a destination address
     * 4. Waits for transaction confirmation
     *
     * @param {string} [sourceAddress] - The source address to use
     * @returns A promise that resolves when the transaction is confirmed
     */
    async function main(sourceAddress?: string) {
        const cdp = new CdpClient();

        // Required: Destination address to send SOL to
        const destinationAddress = "3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE";

        // Amount of lamports to send (default: 1000 = 0.000001 SOL)
        const lamportsToSend = 1000;

        try {
            const connection = new Connection("https://api.devnet.solana.com");

            let fromAddress: string;
            if (sourceAddress) {
                fromAddress = sourceAddress;
                console.log("Using existing SOL account:", fromAddress);
            } else {
                const account = await cdp.solana.createAccount({
                    name: "test-sol-account",
                });

                fromAddress = account.address;
                console.log("Successfully created new SOL account:", fromAddress);

                // Request SOL from faucet
                const faucetResp = await cdp.solana.requestFaucet({
                    address: fromAddress,
                    token: "sol",
                });
                console.log(
                    "Successfully requested SOL from faucet:",
                    faucetResp.signature
                );
            }

            // Wait until the address has balance
            let balance = 0;
            let attempts = 0;
            const maxAttempts = 30;

            while (balance === 0 && attempts < maxAttempts) {
                balance = await connection.getBalance(new PublicKey(fromAddress));
                if (balance === 0) {
                    console.log("Waiting for funds...");
                    await sleep(1000);
                    attempts++;
                }
            }

            if (balance === 0) {
                throw new Error("Account not funded after multiple attempts");
            }

            console.log("Account funded with", balance / 1e9, "SOL");

            if (balance < lamportsToSend) {
                throw new Error(
                    `Insufficient balance: ${balance} lamports, need at least ${lamportsToSend} lamports`
                );
            }

            const transaction = new Transaction();
            transaction.add(
                SystemProgram.transfer({
                    fromPubkey: new PublicKey(fromAddress),
                    toPubkey: new PublicKey(destinationAddress),
                    lamports: lamportsToSend,
                })
            );

            // A more recent blockhash is set in the backend by CDP
            transaction.recentBlockhash = SYSVAR_RECENT_BLOCKHASHES_PUBKEY.toBase58()
            transaction.feePayer = new PublicKey(fromAddress);

            const serializedTx = Buffer.from(
                transaction.serialize({ requireAllSignatures: false })
            ).toString("base64");

            console.log("Transaction serialized successfully");

            const txResult = await cdp.solana.sendTransaction({
                network: "solana-devnet",
                transaction: serializedTx,
            });

            const signature = txResult.signature;
            console.log("Solana transaction hash:", signature);

            console.log("Waiting for transaction to be confirmed");
            const latestBlockhash = await connection.getLatestBlockhash();
            const confirmation = await connection.confirmTransaction({
                signature,
                blockhash: latestBlockhash.blockhash,
                lastValidBlockHeight: latestBlockhash.lastValidBlockHeight,
            });

            if (confirmation.value.err) {
                throw new Error(
                    `Transaction failed: ${confirmation.value.err.toString()}`
                );
            }

            console.log(
                "Transaction confirmed:",
                confirmation.value.err ? "failed" : "success"
            );
            console.log(
                `Transaction explorer link: https://explorer.solana.com/tx/${signature}?cluster=devnet`
            );

            return {
                fromAddress,
                destinationAddress,
                amount: lamportsToSend / 1e9,
                signature,
                success: !confirmation.value.err,
            };
        } catch (error) {
            console.error("Error processing SOL transaction:", error);
            throw error;
        }
    }

    /**
     * Sleeps for a given number of milliseconds
     *
     * @param {number} ms - The number of milliseconds to sleep
     * @returns {Promise<void>} A promise that resolves when the sleep is complete
     */
    function sleep(ms: number): Promise<void> {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

    const sourceAddress = process.argv.length > 2 ? process.argv[2] : undefined;

    main(sourceAddress).catch(console.error);
    ```

    ```python Python theme={null}
    # Usage:
    # uv run python solana/send_transaction.py
    #   [--sender <sender_address>] - optional, if not provided, a new account will be created and funded from the faucet
    #   [--destination <destination_address>] - optional, if not provided, a default destination address will be used
    #   [--amount <amount_in_lamports>] - optional, if not provided, a default amount of 1000 lamports will be used

    import argparse
    import asyncio
    import base64
    import time

    from solana.rpc.api import Client as SolanaClient
    from solders.message import Message
    from solders.hash import Hash
    from solders.signature import Signature
    from solders.pubkey import Pubkey as PublicKey
    from solders.system_program import TransferParams, transfer

    from cdp import CdpClient
    from dotenv import load_dotenv

    load_dotenv()


    async def create_account(cdp: CdpClient):
        print("Creating account...")
        account = await cdp.solana.create_account()
        print(f"Successfully created account: {account.address}")
        return account.address


    async def request_faucet(cdp: CdpClient, address: str):
        print(f"Requesting SOL from faucet for {address}...")
        try:
            response = await cdp.solana.request_faucet(address=address, token="sol")
            transaction_signature = response.transaction_signature
            print(f"Successfully requested SOL from faucet: {transaction_signature}")
            return transaction_signature
        except Exception as e:
            print(f"Faucet request failed: {e}")
            if hasattr(e, "body"):
                print(f"Faucet error body: {e.body}")
            raise


    async def wait_for_balance(connection: SolanaClient, address: str):
        print("Waiting for faucet funds...")
        source_pubkey = PublicKey.from_string(address)

        balance = 0
        max_attempts = 30
        attempts = 0

        while balance == 0 and attempts < max_attempts:
            try:
                balance_resp = connection.get_balance(source_pubkey)
                balance = balance_resp.value
                if balance == 0:
                    print("Waiting for faucet funds...")
                    time.sleep(1)
                else:
                    print(f"Account funded with {balance / 1e9} SOL ({balance} lamports)")
                    return balance
            except Exception as e:
                print(f"Error checking balance: {e}")
                time.sleep(1)
            attempts += 1

        if balance == 0:
            raise ValueError("Timed out waiting for faucet to fund account")

        return balance


    async def send_transaction(
        cdp: CdpClient,
        sender_address: str,
        destination_address: str,
        amount: int = 1000,
    ):
        connection = SolanaClient("https://api.devnet.solana.com")

        source_pubkey = PublicKey.from_string(sender_address)
        dest_pubkey = PublicKey.from_string(destination_address)

        print(
            f"Preparing to send {amount} lamports from {sender_address} to {destination_address}"
        )

        transfer_params = TransferParams(
            from_pubkey=source_pubkey, to_pubkey=dest_pubkey, lamports=amount
        )
        transfer_instr = transfer(transfer_params)

        # A more recent blockhash is set in the backend by CDP
        message = Message.new_with_blockhash(
            [transfer_instr],
            source_pubkey,
            Hash.from_string("SysvarRecentB1ockHashes11111111111111111111"),
        )

        # Create a transaction envelope with signature space
        sig_count = bytes([1])  # 1 byte for signature count (1)
        empty_sig = bytes([0] * 64)  # 64 bytes of zeros for the empty signature
        message_bytes = bytes(message)  # Get the serialized message bytes

        # Concatenate to form the transaction bytes
        tx_bytes = sig_count + empty_sig + message_bytes

        # Encode to base64 used by CDP API
        serialized_tx = base64.b64encode(tx_bytes).decode("utf-8")

        print("Sending transaction to network...")
        tx_resp = await cdp.solana.send_transaction(
            network="solana-devnet",
            transaction=serialized_tx,
        )
        signature = tx_resp.transaction_signature
        print(f"Solana transaction hash: {signature}")

        print("Confirming transaction...")
        confirmation = connection.confirm_transaction(
            Signature.from_string(signature), commitment="processed"
        )

        if hasattr(confirmation, "err") and confirmation.err:
            raise ValueError(f"Transaction failed: {confirmation.err}")

        print(
            f"Transaction confirmed: {'failed' if hasattr(confirmation, 'err') and confirmation.err else 'success'}"
        )
        print(
            f"Transaction explorer link: https://explorer.solana.com/tx/{signature}?cluster=devnet"
        )

        return signature


    async def main():
        parser = argparse.ArgumentParser(description="Solana transfer script")
        parser.add_argument(
            "--sender",
            help="Sender address (if not provided, a new account will be created)",
        )
        parser.add_argument(
            "--destination",
            default="3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE",
            help="Destination address",
        )
        parser.add_argument(
            "--amount",
            type=int,
            default=1000,
            help="Amount in lamports to send (default: 1000)",
        )
        args = parser.parse_args()

        async with CdpClient() as cdp:
            connection = SolanaClient("https://api.devnet.solana.com")

            try:
                sender_address = args.sender

                # If no sender address is provided, create a new account and faucet it
                if not sender_address:
                    print(
                        "No sender address provided. Creating a new account and requesting funds..."
                    )
                    sender_address = await create_account(cdp)
                    await request_faucet(cdp, sender_address)
                    await wait_for_balance(connection, sender_address)
                else:
                    print(f"Using provided sender address: {sender_address}")
                    # Check if there's a balance
                    source_pubkey = PublicKey.from_string(sender_address)
                    balance_resp = connection.get_balance(source_pubkey)
                    balance = balance_resp.value
                    print(
                        f"Sender account balance: {balance / 1e9} SOL ({balance} lamports)"
                    )

                    if balance == 0:
                        print("Account has zero balance, requesting funds from faucet...")
                        await request_faucet(cdp, sender_address)
                        await wait_for_balance(connection, sender_address)

                await send_transaction(cdp, sender_address, args.destination, args.amount)

            except Exception as error:
                print(f"Error in process: {error}")


    asyncio.run(main())
    ```
  </CodeGroup>
</Accordion>

<Tip>
  More code samples are available in our [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/README.md)
  and [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/README.md) SDK repositories.
</Tip>

## Optimizing transaction sends

### Priority Fee

When sending a transaction on Solana, you can set a priority fee, which is an optional fee that increases the likelihood of your transaction being included in the next block by validators.
The priority fee is calculated based on the *compute unit price* and *compute unit limit* of the transaction.

*Priority Fee* = *Compute Unit Limit* × *Compute Unit Price*

Read more about [Solana's fee model](https://solana.com/docs/core/fees).

<Tip>
  CDP v2 Server Wallet will automatically add the appropriate instructions for the *compute unit limit* and *compute unit price* on a transaction if not already present.
</Tip>

To set your own  *compute unit limit* and *compute unit price* for a transaction, take a look at the examples below.

#### Compute Unit Price

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { ComputeBudgetProgram, Transaction } from "@solana/web3.js";

  // Assume you already have `otherInstruction`.
  // Build a tx with compute unit price first, then your instruction(s).
  const computeUnitPriceInstruction = ComputeBudgetProgram.setComputeUnitPrice({
    microLamports: 5000,
  });

  const tx = new Transaction().add(priorityFeeInstruction, otherInstruction);

  // Send tx with your usual send flow.
  ```

  ```python Python theme={null}
  from solana.transaction import Transaction
  from solders.compute_budget import set_compute_unit_price

  # Assume you already have `other_instruction`.
  # Build a tx with compute unit price first, then your instruction(s).
  priority_fee_instruction = set_compute_unit_price(5000)

  tx = Transaction().add(priority_fee_instruction, your_instruction)

  # Send tx with your usual send flow.
  ```
</CodeGroup>

#### Compute Unit Limit

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { ComputeBudgetProgram, Transaction } from "@solana/web3.js";

  // Assume you already have `otherInstruction`.
  // Build a tx with compute unit limit first, then your instruction(s).
  const computeLimitInstruction = ComputeBudgetProgram.setComputeUnitLimit({
    units: 300000,
  });

  const tx = new Transaction().add(computeLimitInstruction, otherInstruction);

  // Send tx with your usual send flow.
  ```

  ```python Python theme={null}
  from solana.transaction import Transaction
  from solders.compute_budget import set_compute_unit_limit

  # Assume you already have `other_instruction`
  # Build a tx with compute unit limit first, then your instruction(s).
  compute_limit_instruction = set_compute_unit_limit(300000)

  tx = Transaction().add(compute_limit_instruction, other_instruction)

  # Send tx with your usual send flow.
  ```
</CodeGroup>

## Bring your own node

Use a custom node provider to build and broadcast the transaction instead of relying on the CDP SDK.
You will still call CDP to sign the transaction, but you can query the recent blockhash and broadcast the transaction using your own node.

<Accordion title="How CDP handles transaction signing">
  When you call `cdp.solana.signTransaction()`, you send an unsigned transaction to CDP's secure infrastructure. CDP signs it using your managed private key (which never leaves the [Trusted Execution Environment](/server-wallets/v2/introduction/security#tee-architecture)) and returns the signed transaction.
</Accordion>

<Accordion title="View a complete example on using your own node">
  <CodeGroup>
    ```typescript TypeScript highlight={33} theme={null}
    // Usage: pnpm tsx solana/signAndSendTransaction.ts [sourceAddress]

    import { CdpClient } from "@coinbase/cdp-sdk";
    import "dotenv/config";

    import {
      Connection,
      PublicKey,
      SystemProgram,
      Transaction,
    } from "@solana/web3.js";

    /**
     * This script will:
     * 1. Either use a provided Solana address or create a new one
     * 2. If a new account is created, requests SOL from CDP faucet
     * 3. Signs a transaction with CDP to send SOL to a destination address
     * 4. Broadcasts the signed transaction
     *
     * @param {string} [sourceAddress] - The source address to use
     * @returns A promise that resolves when the transaction is confirmed
     */
    async function main(sourceAddress?: string) {
      const cdp = new CdpClient();

      // Required: Destination address to send SOL to (replace with your recipient)
      const destinationAddress = "3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE";

      // Amount of lamports to send (default: 1000 = 0.000001 SOL)
      const lamportsToSend = 1000;

      try {
        const connection = new Connection("https://api.devnet.solana.com");

        let fromAddress: string;
        if (sourceAddress) {
          fromAddress = sourceAddress;
          console.log("Using existing SOL account:", fromAddress);
        } else {
          const account = await cdp.solana.createAccount({
            name: "test-sol-account",
          });

          fromAddress = account.address;
          console.log("Successfully created new SOL account:", fromAddress);

          // Request SOL from faucet
          const faucetResp = await cdp.solana.requestFaucet({
            address: fromAddress,
            token: "sol",
          });
          console.log(
            "Successfully requested SOL from faucet:",
            faucetResp.signature
          );
        }

        // Wait until the address has balance
        let balance = 0;
        let attempts = 0;
        const maxAttempts = 30;

        while (balance === 0 && attempts < maxAttempts) {
          balance = await connection.getBalance(new PublicKey(fromAddress));
          if (balance === 0) {
            console.log("Waiting for funds...");
            await sleep(1000);
            attempts++;
          }
        }

        if (balance === 0) {
          throw new Error("Account not funded after multiple attempts");
        }

        console.log("Account funded with", balance / 1e9, "SOL");

        if (balance < lamportsToSend) {
          throw new Error(
            `Insufficient balance: ${balance} lamports, need at least ${lamportsToSend} lamports`
          );
        }

        const { blockhash } = await connection.getLatestBlockhash();

        const transaction = new Transaction();
        transaction.add(
          SystemProgram.transfer({
            fromPubkey: new PublicKey(fromAddress),
            toPubkey: new PublicKey(destinationAddress),
            lamports: lamportsToSend,
          })
        );

        transaction.recentBlockhash = blockhash;
        transaction.feePayer = new PublicKey(fromAddress);

        const serializedTx = Buffer.from(
          transaction.serialize({ requireAllSignatures: false })
        ).toString("base64");

        console.log("Transaction serialized successfully");

        const signedTxResponse = await cdp.solana.signTransaction({
          address: fromAddress,
          transaction: serializedTx,
        });

        const decodedSignedTx = Buffer.from(signedTxResponse.signature, "base64");

        const signature = await connection.sendRawTransaction(decodedSignedTx);
        console.log("Solana transaction hash:", signature);

        console.log("Waiting for transaction to be confirmed");
        const latestBlockhash = await connection.getLatestBlockhash();
        const confirmation = await connection.confirmTransaction({
          signature,
          blockhash: latestBlockhash.blockhash,
          lastValidBlockHeight: latestBlockhash.lastValidBlockHeight,
        });

        if (confirmation.value.err) {
          throw new Error(
            `Transaction failed: ${confirmation.value.err.toString()}`
          );
        }

        console.log(
          "Transaction confirmed:",
          confirmation.value.err ? "failed" : "success"
        );
        console.log(
          `Transaction explorer link: https://explorer.solana.com/tx/${signature}?cluster=devnet`
        );

        return {
          fromAddress,
          destinationAddress,
          amount: lamportsToSend / 1e9,
          signature,
          success: !confirmation.value.err,
        };
      } catch (error) {
        console.error("Error processing SOL transaction:", error);
        throw error;
      }
    }

    /**
     * Sleeps for a given number of milliseconds
     *
     * @param {number} ms - The number of milliseconds to sleep
     * @returns {Promise<void>} A promise that resolves when the sleep is complete
     */
    function sleep(ms: number): Promise<void> {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }

    const sourceAddress = process.argv.length > 2 ? process.argv[2] : undefined;

    main(sourceAddress).catch(console.error);
    ```

    ```python Python highlight={80,175} theme={null}
    # Usage:
    # uv run python solana/send_transaction.py
    #   [--sender <sender_address>] - optional, if not provided, a new account will be created and funded from the faucet
    #   [--destination <destination_address>] - optional, if not provided, a default destination address will be used
    #   [--amount <amount_in_lamports>] - optional, if not provided, a default amount of 1000 lamports will be used

    import argparse
    import asyncio
    import base64
    import time

    from solana.rpc.api import Client as SolanaClient
    from solana.rpc.types import TxOpts
    from solders.message import Message
    from solders.pubkey import Pubkey as PublicKey
    from solders.system_program import TransferParams, transfer

    from cdp import CdpClient
    from dotenv import load_dotenv

    load_dotenv()


    async def create_account(cdp: CdpClient):
        print("Creating account...")
        account = await cdp.solana.create_account()
        print(f"Successfully created account: {account.address}")
        return account.address


    async def request_faucet(cdp: CdpClient, address: str):
        print(f"Requesting SOL from faucet for {address}...")
        try:
            response = await cdp.solana.request_faucet(address=address, token="sol")
            transaction_signature = response.transaction_signature
            print(f"Successfully requested SOL from faucet: {transaction_signature}")
            return transaction_signature
        except Exception as e:
            print(f"Faucet request failed: {e}")
            if hasattr(e, "body"):
                print(f"Faucet error body: {e.body}")
            raise


    async def wait_for_balance(connection: SolanaClient, address: str):
        print("Waiting for faucet funds...")
        source_pubkey = PublicKey.from_string(address)

        balance = 0
        max_attempts = 30
        attempts = 0

        while balance == 0 and attempts < max_attempts:
            try:
                balance_resp = connection.get_balance(source_pubkey)
                balance = balance_resp.value
                if balance == 0:
                    print("Waiting for faucet funds...")
                    time.sleep(1)
                else:
                    print(f"Account funded with {balance / 1e9} SOL ({balance} lamports)")
                    return balance
            except Exception as e:
                print(f"Error checking balance: {e}")
                time.sleep(1)
            attempts += 1

        if balance == 0:
            raise ValueError("Timed out waiting for faucet to fund account")

        return balance


    async def send_transaction(
        cdp: CdpClient,
        sender_address: str,
        destination_address: str,
        amount: int = 1000,
    ):
        connection = SolanaClient("https://api.devnet.solana.com")

        source_pubkey = PublicKey.from_string(sender_address)
        dest_pubkey = PublicKey.from_string(destination_address)

        print(
            f"Preparing to send {amount} lamports from {sender_address} to {destination_address}"
        )

        blockhash_resp = connection.get_latest_blockhash()
        blockhash = blockhash_resp.value.blockhash

        transfer_params = TransferParams(
            from_pubkey=source_pubkey, to_pubkey=dest_pubkey, lamports=amount
        )
        transfer_instr = transfer(transfer_params)

        message = Message.new_with_blockhash(
            [transfer_instr],
            source_pubkey,
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

        print("Signing transaction...")

        try:
            response = await cdp.solana.sign_transaction(
                sender_address, transaction=serialized_tx
            )
            signed_tx = response.signed_transaction
            print("Transaction signed successfully")
        except Exception as e:
            print(f"Error signing transaction: {e}")
            if hasattr(e, "body"):
                print(f"Error body: {e.body}")
            raise

        # Decode the signed transaction from base64
        decoded_signed_tx = base64.b64decode(signed_tx)

        print("Sending transaction to network...")
        tx_resp = connection.send_raw_transaction(
            decoded_signed_tx,
            opts=TxOpts(skip_preflight=False, preflight_commitment="processed"),
        )
        signature = tx_resp.value
        print(f"Solana transaction hash: {signature}")

        print("Confirming transaction...")
        confirmation = connection.confirm_transaction(signature, commitment="processed")

        if hasattr(confirmation, "err") and confirmation.err:
            raise ValueError(f"Transaction failed: {confirmation.err}")

        print(
            f"Transaction confirmed: {'failed' if hasattr(confirmation, 'err') and confirmation.err else 'success'}"
        )
        print(
            f"Transaction explorer link: https://explorer.solana.com/tx/{signature}?cluster=devnet"
        )

        return signature


    async def main():
        parser = argparse.ArgumentParser(description="Solana transfer script")
        parser.add_argument(
            "--sender",
            help="Sender address (if not provided, a new account will be created)",
        )
        parser.add_argument(
            "--destination",
            default="3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE",
            help="Destination address",
        )
        parser.add_argument(
            "--amount",
            type=int,
            default=1000,
            help="Amount in lamports to send (default: 1000)",
        )
        args = parser.parse_args()

        async with CdpClient() as cdp:
            connection = SolanaClient("https://api.devnet.solana.com")

            try:
                sender_address = args.sender

                # If no sender address is provided, create a new account and faucet it
                if not sender_address:
                    print(
                        "No sender address provided. Creating a new account and requesting funds..."
                    )
                    sender_address = await create_account(cdp)
                    await request_faucet(cdp, sender_address)
                    await wait_for_balance(connection, sender_address)
                else:
                    print(f"Using provided sender address: {sender_address}")
                    # Check if there's a balance
                    source_pubkey = PublicKey.from_string(sender_address)
                    balance_resp = connection.get_balance(source_pubkey)
                    balance = balance_resp.value
                    print(
                        f"Sender account balance: {balance / 1e9} SOL ({balance} lamports)"
                    )

                    if balance == 0:
                        print("Account has zero balance, requesting funds from faucet...")
                        await request_faucet(cdp, sender_address)
                        await wait_for_balance(connection, sender_address)

                await send_transaction(cdp, sender_address, args.destination, args.amount)

            except Exception as error:
                print(f"Error in process: {error}")


    asyncio.run(main())
    ```
  </CodeGroup>
</Accordion>

## What to read next

* [Batching instructions](/server-wallets/v2/solana-features/batching-instructions): Learn how to batch multiple instructions efficiently
* [Sponsor transactions](/server-wallets/v2/solana-features/sponsor-transactions): Implement fee sponsorship for better UX
* [Solana accounts](/server-wallets/v2/introduction/accounts#solana-accounts): Understand Solana account management in CDP
* [API reference](/api-reference/v2/authentication): Complete API documentation for all Solana operations

