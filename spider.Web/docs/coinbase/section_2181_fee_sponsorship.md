# Fee Sponsorship
Source: https://docs.cdp.coinbase.com/server-wallets/v2/solana-features/sponsor-transactions



## Overview

Fee sponsorship lets CDP pay the Solana network fee on behalf of your server wallet.
Your wallet can send transactions without holding SOL to cover gas.

This feature is in private preview and available to enterprise-scale integrations only.
To opt in, [apply for access](https://docs.google.com/forms/d/e/1FAIpQLSdMG0DDGkLDV73H1QNVQ50hrjVRBtNgfBPwVVW_f8RAASoWgQ/viewform).
Once approved, pass `useCdpSponsor: true` when calling `sendTransaction`.

## Sponsoring a transaction

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import {
    address as solanaAddress,
    appendTransactionMessageInstructions,
    compileTransaction,
    createNoopSigner,
    createTransactionMessage,
    getBase64EncodedWireTransaction,
    pipe,
    setTransactionMessageFeePayer,
    setTransactionMessageLifetimeUsingBlockhash,
  } from "@solana/kit";
  import { getTransferSolInstruction } from "@solana-program/system";

  const cdp = new CdpClient();

  const account = await cdp.solana.getOrCreateAccount({ name: "my-account" });

  // A more recent blockhash is set in the backend by CDP
  const FAKE_BLOCKHASH = "SysvarRecentB1ockHashes11111111111111111111";

  const instruction = getTransferSolInstruction({
    source: createNoopSigner(solanaAddress(account.address)),
    destination: solanaAddress("3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE"),
    amount: 1000n,
  });

  const txMsg = pipe(
    createTransactionMessage({ version: 0 }),
    (tx) => setTransactionMessageFeePayer(solanaAddress(account.address), tx),
    (tx) =>
      setTransactionMessageLifetimeUsingBlockhash(
        { blockhash: FAKE_BLOCKHASH, lastValidBlockHeight: 9999999n },
        tx,
      ),
    (tx) => appendTransactionMessageInstructions([instruction], tx),
  );

  const serializedTx = getBase64EncodedWireTransaction(compileTransaction(txMsg));

  const result = await cdp.solana.sendTransaction({
    network: "solana-mainnet",
    transaction: serializedTx,
    useCdpSponsor: true,
  });

  console.log("Transaction signature:", result.transactionSignature);
  ```

  ```python Python theme={null}
  import base64
  import asyncio

  from solders.pubkey import Pubkey as PublicKey
  from solders.system_program import TransferParams, transfer
  from solders.message import Message
  from solders.hash import Hash

  from cdp import CdpClient

  async def main():
      async with CdpClient() as cdp:
          account = await cdp.solana.get_or_create_account(name="my-account")

          source_pubkey = PublicKey.from_string(account.address)
          dest_pubkey = PublicKey.from_string("3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE")

          # A more recent blockhash is set in the backend by CDP
          fake_blockhash = Hash.from_string("SysvarRecentB1ockHashes11111111111111111111")

          transfer_instr = transfer(TransferParams(
              from_pubkey=source_pubkey,
              to_pubkey=dest_pubkey,
              lamports=1000,
          ))

          message = Message.new_with_blockhash([transfer_instr], source_pubkey, fake_blockhash)

          sig_count = bytes([1])
          empty_sig = bytes([0] * 64)
          serialized_tx = base64.b64encode(sig_count + empty_sig + bytes(message)).decode("utf-8")

          response = await cdp.solana.send_transaction(
              network="solana-mainnet",
              transaction=serialized_tx,
              use_cdp_sponsor=True,
          )

          print(f"Transaction signature: {response.transaction_signature}")

  asyncio.run(main())
  ```
</CodeGroup>

## Rate limits

CDP enforces per-project sponsorship limits. If a limit is exceeded, the API returns a `429` response. To request a limit increase, reach out in the [Coinbase Developer Discord](https://discord.gg/cdp).

***

## Advanced: Manual fee payer orchestration

If you need full control over fee payment, for example, to use an external relayer or to designate a specific CDP account as the fee payer for other accounts, you can manage the fee payer yourself without `useCdpSponsor`.

This approach requires:

1. A dedicated fee payer account with SOL for gas
2. Building a transaction with `feePayer` set to that account
3. Signing with both the sender and the fee payer
4. Broadcasting the fully-signed transaction

<CodeGroup>
  ```ts TypeScript lines wrap [expandable] theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";
      import "dotenv/config";

      import {
        Connection,
        PublicKey,
        SystemProgram,
        Transaction,
      } from "@solana/web3.js";

      async function main(sourceAddress?: string) {
        const cdp = new CdpClient();

        // Required: Destination address to send SOL to
        const destinationAddress = "3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE";

        // Amount of lamports to send (default: 1000 = 0.000001 SOL)
        const lamportsToSend = 1000;

        try {
          const connection = new Connection("https://api.devnet.solana.com");

          // Set up a dedicated fee payer account.
          const feePayer = await cdp.solana.getOrCreateAccount({
            name: "test-sol-account-fee-payer",
          });
          console.log("Fee payer address: " + feePayer.address);

          // Request funds on the feePayer address to pay for the gas.
          await requestFaucetAndWaitForBalance(cdp, feePayer.address, connection);

          let fromAddress: string;
          if (sourceAddress) {
            fromAddress = sourceAddress;
            console.log("Using existing SOL account:", fromAddress);
          } else {
            // Set up a source account.
            const account = await cdp.solana.getOrCreateAccount({
              name: "test-sol-account",
            })

            fromAddress = account.address;
            console.log("Successfully created new SOL account:", fromAddress);

            // Request funds on the source account for transaction amount.
            await requestFaucetAndWaitForBalance(cdp, fromAddress, connection);
          }

          const balance = await connection.getBalance(new PublicKey(fromAddress));
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

          const { blockhash } = await connection.getLatestBlockhash();
          transaction.recentBlockhash = blockhash;
          transaction.feePayer = new PublicKey(feePayer.address);

          const serializedTx = Buffer.from(
            transaction.serialize({ requireAllSignatures: false })
          ).toString("base64");

          // Sign with the funding account.
          const signedTxResponse = await cdp.solana.signTransaction({
            address: fromAddress,
            transaction: serializedTx,
          });

          const signedBase64Tx = signedTxResponse.signature;

          // Sign with the feePayer account.
          const finalSignedTxResponse = await cdp.solana.signTransaction({
            address: feePayer.address,
            transaction: signedBase64Tx,
          });

          // Send the signed transaction to the network.
          const signature = await connection.sendRawTransaction(Buffer.from(finalSignedTxResponse.signature, 'base64'));

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


      /**
       * Requests funds from the faucet and waits for the balance to be available
       *
       * @param {CdpClient} cdp - The CDP client instance
       * @param {string} address - The address to fund
       * @param {Connection} connection - The Solana connection
       * @param {string} token - The token to request (default: "sol")
       * @returns {Promise<void>} A promise that resolves when the account is funded
       */
      async function requestFaucetAndWaitForBalance(
          cdp: CdpClient,
          address: string,
          connection: Connection,
      ): Promise<void> {
        // Request funds from faucet
        const faucetResp = await cdp.solana.requestFaucet({
          address: address,
          token: "sol",
        });
        console.log(
            `Successfully requested SOL from faucet:`,
            faucetResp.signature
        );

        // Wait until the address has balance
        let balance = 0;
        let attempts = 0;
        const maxAttempts = 30;

        while (balance === 0 && attempts < maxAttempts) {
          balance = await connection.getBalance(new PublicKey(address));
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
        return;
      }


      const sourceAddress = process.argv.length > 2 ? process.argv[2] : undefined;

      main(sourceAddress).catch(console.error);
  ```

  ```python Python lines wrap [expandable] theme={null}
      import asyncio
      import base64
      from decimal import Decimal

      from solders.pubkey import Pubkey as PublicKey
      from solders.system_program import TransferParams, transfer
      from solders.message import Message
      from solana.rpc.api import Client as SolanaClient
      from solana.rpc.types import TxOpts

      from cdp import CdpClient

      async def main(source_address: str = None):
          """Main function to demonstrate sending SOL with a fee payer."""
          cdp = CdpClient()

          try:
              # Required: Destination address to send SOL to
              destination_address = "3KzDtddx4i53FBkvCzuDmRbaMozTZoJBb1TToWhz3JfE"

              # Amount of lamports to send (default: 1000 = 0.000001 SOL)
              lamports_to_send = 1000

              connection = SolanaClient("https://api.devnet.solana.com")

              # Create or get fee payer account
              fee_payer = await cdp.solana.get_or_create_account(
                  name="test-sol-account-relayer"
              )
              print(f"Fee payer address: {fee_payer.address}")

              # Request funds on the feePayer address
              await request_faucet_and_wait_for_balance(cdp, fee_payer.address, connection)

              # Get or create funding account
              if source_address:
                  from_address = source_address
                  print(f"Using existing SOL account: {from_address}")
              else:
                  account = await cdp.solana.get_or_create_account(
                      name="test-sol-account"
                  )
                  from_address = account.address
                  print(f"Successfully created new SOL account: {from_address}")

                  # Request funds to send on the from address
                  await request_faucet_and_wait_for_balance(cdp, from_address, connection)

              # Check initial balance
              initial_from_balance = connection.get_balance(PublicKey.from_string(from_address)).value
              if initial_from_balance < lamports_to_send:
                  raise Exception(
                      f"Insufficient balance: {initial_from_balance} lamports, need at least {lamports_to_send} lamports"
                  )

              # Create transaction
              source_pubkey = PublicKey.from_string(from_address)
              dest_pubkey = PublicKey.from_string(destination_address)
              fee_payer_pubkey = PublicKey.from_string(fee_payer.address)

              # Get latest blockhash
              blockhash_resp = connection.get_latest_blockhash()
              blockhash = blockhash_resp.value.blockhash

              # Create transfer instruction
              transfer_params = TransferParams(
                  from_pubkey=source_pubkey,
                  to_pubkey=dest_pubkey,
                  lamports=lamports_to_send
              )
              transfer_instr = transfer(transfer_params)

              # Create message
              message = Message.new_with_blockhash(
                  [transfer_instr],
                  fee_payer_pubkey,  # Set fee payer
                  blockhash,
              )

              # Get initial balances before transaction
              initial_fee_payer_balance = connection.get_balance(fee_payer_pubkey).value

              # Create a transaction envelope with signature space
              sig_count = bytes([2])  # 2 bytes for signature count (2 signatures needed)
              empty_sig = bytes([0] * 128)  # 128 bytes of zeros for the empty signatures (2 * 64)
              message_bytes = bytes(message)  # Get the serialized message bytes

              # Concatenate to form the transaction bytes
              tx_bytes = sig_count + empty_sig + message_bytes

              # Encode to base64 used by CDP API
              serialized_tx = base64.b64encode(tx_bytes).decode("utf-8")

              # Sign with the funding account
              signed_tx_response = await cdp.solana.sign_transaction(
                  address=from_address,
                  transaction=serialized_tx
              )

              # Sign with fee payer address
              final_signed_tx_response = await cdp.solana.sign_transaction(
                  address=fee_payer.address,
                  transaction=signed_tx_response.signed_transaction
              )

              # Send the signed transaction to the network
              send_response = connection.send_raw_transaction(
                  base64.b64decode(final_signed_tx_response.signed_transaction),
                  opts=TxOpts(skip_preflight=False, preflight_commitment="processed")
              )
              signature = send_response.value

              # Wait for confirmation
              confirmation = connection.confirm_transaction(
                  signature,
                  commitment="processed"
              )

              if hasattr(confirmation, "err") and confirmation.err:
                  raise Exception(f"Transaction failed: {confirmation.err}")

              print("Transaction confirmed:", "failed" if hasattr(confirmation, "err") and confirmation.err else "success")
              print(f"Transaction explorer link: https://explorer.solana.com/tx/{signature}?cluster=devnet")

              return {
                  "from_address": from_address,
                  "destination_address": destination_address,
                  "amount": lamports_to_send / 1e9,
                  "signature": signature,
                  "success": not (hasattr(confirmation, "err") and confirmation.err),
              }

          except Exception as error:
              print("Error processing SOL transaction:", error)
              raise error
          finally:
              # Clean up the CDP client session
              await cdp.close()

      async def request_faucet_and_wait_for_balance(cdp, address, connection, token="sol"):
          """Request funds from the faucet and wait for the balance to be available."""
          # Request funds from faucet
          faucet_resp = await cdp.solana.request_faucet(
              address=address,
              token=token
          )
          print(f"Successfully requested {token.upper()} from faucet:", faucet_resp)

          # Wait until the address has balance
          balance = 0
          attempts = 0
          max_attempts = 30

          while balance == 0 and attempts < max_attempts:
              balance = connection.get_balance(PublicKey.from_string(address)).value
              if balance == 0:
                  print("Waiting for funds...")
                  await asyncio.sleep(1)
                  attempts += 1

          if balance == 0:
              raise Exception("Account not funded after multiple attempts")

          print("Account funded with", balance / 1e9, "SOL")
          return

      if __name__ == "__main__":
          import sys
          source_address = sys.argv[1] if len(sys.argv) > 1 else None
          asyncio.run(main(source_address))
  ```
</CodeGroup>

## What to read next

* [Sending Transactions](/server-wallets/v2/solana-features/sending-transactions): Send Solana transactions without fee sponsorship
* [Batching Instructions](/server-wallets/v2/solana-features/batching-instructions): Batch multiple instructions into a single transaction

