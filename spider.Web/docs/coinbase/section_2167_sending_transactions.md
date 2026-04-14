# Sending Transactions
Source: https://docs.cdp.coinbase.com/server-wallets/v2/evm-features/sending-transactions



The [CDP SDK's](https://github.com/coinbase/cdp-sdk) `sendTransaction` method handles **gas estimation**, **nonce management**, **transaction signing**,
and **broadcasting** for EVM accounts. This means that you don't need to specify these details when you submit
a transaction onchain. CDP's nonce management system ensures that the nonce is set correctly for each transaction,
and the gas price is estimated to ensure that the transaction is sent at a reasonable price.

You can read more about the `sendTransaction` API in the [API Reference](/api-reference/v2/rest-api/evm-accounts/send-a-transaction).

<Tip>
  The SendTransaction API, which handles both signing and broadcasting, is currently supported only on Base, Ethereum, Avalanche, Polygon, Optimism and Arbitrum.

  For other networks, use the SignTransaction API for signing and rely on your own RPC URLs to broadcast transactions as shown [here](https://docs.cdp.coinbase.com/server-wallets/v2/evm-features/managed-mode#bring-your-own-node).
</Tip>

The following code snippet demonstrates how to send a transaction using the `sendTransaction` method.
You can also refer to our example code in
[Typescript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/sendManyTransactions.ts) and
[Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/send_transaction.py).

<CodeGroup>
  ```ts TypeScript lines wrap [expandable] theme={null}
  import dotenv from "dotenv";
  import { parseEther, createPublicClient, http } from "viem";
  import { baseSepolia } from "viem/chains";

  import { CdpClient } from "@coinbase/cdp-sdk";

  dotenv.config();

  /**
   * This script demonstrates using the new sendTransaction method to:
   * 1. Create a new ethereum account on CDP
   * 2. Request ETH from CDP faucet
   * 3. Sign and send a transaction in a single method call.
   */
  async function main() {
    const cdp = new CdpClient();
    const publicClient = createPublicClient({ chain: baseSepolia, transport: http() });

    // Step 1: Create a new EVM account
    const evmAccount = await cdp.evm.createAccount();
    console.log("Successfully created EVM account:", evmAccount.address);

    // Step 2: Request ETH from the faucet
    const faucetResp = await cdp.evm.requestFaucet({
      address: evmAccount.address,
      network: "base-sepolia",
      token: "eth",
    });

    // Wait for the faucet transaction to be confirmed onchain.
    const faucetTxReceipt = await publicClient.waitForTransactionReceipt({
      hash: faucetResp.transactionHash,
    });

    console.log("Successfully requested ETH from faucet:", faucetTxReceipt.transactionHash);

    // Step 3: Sign and send the transaction in a single step with sendTransaction.
    // The API will automatically estimate the gas price and determine the nonce.
    const txResult = await cdp.evm.sendTransaction({
      address: evmAccount.address,
      network: "base-sepolia",
      transaction: {
        to: "0x4252e0c9A3da5A2700e7d91cb50aEf522D0C6Fe8", // recipient address
        value: parseEther("0.000001"), // sending 0.000001 ETH
      },
    });

    console.log("Transaction sent successfully!");
    console.log(
      `Transaction explorer link: https://sepolia.basescan.org/tx/${txResult.transactionHash}`,
    );

    await publicClient.waitForTransactionReceipt({ hash: txResult.transactionHash });

    console.log("Transaction confirmed!");
  }

  main().catch(console.error);
  ```

  ```python Python lines wrap [expandable] theme={null}
  import asyncio

  from web3 import Web3

  from cdp import CdpClient
  from cdp.evm_transaction_types import TransactionRequestEIP1559

  import dotenv

  dotenv.load_dotenv()

  w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))

  # This script demonstrates using the send_transaction API to:
  # 1. Create an EVM account
  # 2. Request ETH from the faucet
  # 3. Sign and send a transaction in a single method call.
  async def main():
      async with CdpClient() as cdp:
          # Step 1: Create an EVM account
          account = await cdp.evm.create_account()
          print(f"Created account: {account.address}")

          # Step 2: Request ETH from the faucet
          faucet_hash = await cdp.evm.request_faucet(
              address=account.address, network="base-sepolia", token="eth"
          )

          w3.eth.wait_for_transaction_receipt(faucet_hash)
          print(f"Received funds from faucet for address: {account.address}")

          # Step 3: Sign and send the transaction in a single step with send_transaction.
          # The API will automatically estimate the gas price and determine the nonce.
          tx_hash = await cdp.evm.send_transaction(
              address=account.address,
              transaction=TransactionRequestEIP1559(
                  to="0x0000000000000000000000000000000000000000",
                  value=w3.to_wei(0.000001, "ether"),
              ),
              network="base-sepolia",
          )

          print(f"Transaction sent! Hash: {tx_hash}")
          print("Waiting for transaction confirmation...")

          tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
          status = "Success" if tx_receipt.status == 1 else "Failed"

          print(f"Transaction confirmed in block {tx_receipt.blockNumber}")
          print(f"Transaction status: {status}")


  asyncio.run(main())
  ```
</CodeGroup>

