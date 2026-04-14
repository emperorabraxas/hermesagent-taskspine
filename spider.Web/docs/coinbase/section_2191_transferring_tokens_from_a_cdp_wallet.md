# Transferring tokens from a CDP Wallet
Source: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/transfers



## Overview

A **transfer** refers to sending tokens from one account to another on a blockchain network.

Token transfers are supported on EVM Accounts, EVM Smart Accounts and Solana Accounts.
EVM Accounts can transfer native ETH or ERC-20 tokens, and Solana Accounts can transfer native SOL or SPL tokens.

## Prerequisites

* Python 3.10+ or Node.js 20+
* CDP API credentials (See the [Quickstart](/server-wallets/v2/introduction/quickstart#create-keys) guide for more information)
* Required packages:

<CodeGroup>
  ```bash TypeScript lines wrap theme={null}
  npm install @coinbase/cdp-sdk viem
  ```

  ```bash Python lines wrap theme={null}
  pip install cdp-sdk web3
  ```
</CodeGroup>

If you're using Solana, you'll want to install `@solana/web3.js` instead of `viem` on TypeScript, and `solana` instead of `web3` on Python:

<CodeGroup>
  ```bash TypeScript lines wrap theme={null}
  npm install @coinbase/cdp-sdk @solana/web3.js
  ```

  ```bash Python lines wrap theme={null}
  pip install cdp-sdk solana
  ```
</CodeGroup>

<Tip>
  If you complete the [Quickstart](/server-wallets/v2/introduction/quickstart), you will have a complete working setup to complete this tutorial.
</Tip>

## EVM Account transfer

This section will walk you through transferring funds from an externally owned account (EOA).

### 1. Create accounts

First, create two EOAs:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  const sender = await cdp.evm.getOrCreateAccount({ name: "Sender" });
  const receiver = await cdp.evm.getOrCreateAccount({ name: "Receiver" });
  ```

  ```python Python lines wrap theme={null}
  sender = await cdp.evm.get_or_create_account(name="Sender")
  receiver = await cdp.evm.get_or_create_account(name="Receiver")
  ```
</CodeGroup>

### 2. Transfer ETH to account

Next, transfer ETH using the accounts you created earlier.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { parseEther } from "viem";

  const { transactionHash } = await sender.transfer({
  to: receiver,
  amount: parseEther("0.00001"),
  token: "eth",
  network: "base-sepolia"
  });
  ```

  ```python Python lines wrap theme={null}
  from web3 import Web3

  tx_hash = await sender.transfer(
  to=receiver,
  amount=Web3.toWei("0.00001", "ether"),
  token="eth",
  network="base-sepolia"
  )
  ```
</CodeGroup>

### 3. Wait for transfer result

Finally, wait for the transfer to be confirmed.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { createPublicClient, http } from "viem";
  import { baseSepolia } from "viem/chains";

  const publicClient = createPublicClient({
  chain: baseSepolia,
  transport: http(),
  });

  const receipt = await publicClient.waitForTransactionReceipt({
  hash: transactionHash,
  });
  ```

  ```python Python lines wrap theme={null}
  from web3 import Web3

  w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  ```
</CodeGroup>

## Smart Account transfer

This section will walk you through transferring funds from a Smart Account to an EOA.

### 1. Create Smart Account

First, we create an owner account to assign to our newly created Smart Account:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  const sender = await cdp.evm.createSmartAccount({
  owner: await cdp.evm.getOrCreateAccount({ name: "Owner" })
  });
  ```

  ```python Python lines wrap theme={null}
  owner = await cdp.evm.get_or_create_account(name="Owner")
  sender = await cdp.evm.create_smart_account(owner=owner)
  ```
</CodeGroup>

### 2. Create receiver account

Create a receiver account:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  const receiver = await cdp.evm.getOrCreateAccount({ name: "Receiver" });
  ```

  ```python Python lines wrap theme={null}
  receiver = await cdp.evm.get_or_create_account(name="Receiver")
  ```
</CodeGroup>

### 3. Transfer ETH to account

Perform the transfer using the smart account:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { parseEther } from "viem";

  const { userOpHash } = await sender.transfer({
  to: receiver,
  amount: parseEther("0.00001"),
  token: "eth",
  network: "base-sepolia"
  });
  ```

  ```python Python theme={null}
  from web3 import Web3

  transfer_result = await sender.transfer(
  to=receiver,
  amount=Web3.toWei("0.00001", "ether"),
  token="eth",
  network="base-sepolia"
  )
  ```
</CodeGroup>

### 4. Wait for transfer result

Finally, wait for the transfer to be confirmed.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  const receipt = await sender.waitForUserOperation({
  userOpHash,
  });
  ```

  ```python Python lines wrap theme={null}
  receipt = await sender.wait_for_user_operation(
  user_op_hash=transfer_result.user_op_hash
  )
  ```
</CodeGroup>

## Solana Account transfer

This section will walk you through transferring funds from a Solana Account.

### 1. Create accounts

First, create two Solana Accounts:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  const sender = await cdp.solana.getOrCreateAccount({ name: "Sender" });
  const receiver = await cdp.solana.getOrCreateAccount({ name: "Receiver" });
  ```

  ```python Python lines wrap theme={null}
  sender = await cdp.solana.get_or_create_account(name="Sender")
  receiver = await cdp.solana.get_or_create_account(name="Receiver")
  ```
</CodeGroup>

### 2. Transfer SOL to account

Perform the transfer using the Solana Account:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { LAMPORTS_PER_SOL } from "@solana/web3.js";

  const { signature } = await sender.transfer({
  to: receiver,
  amount: 0.0001 * LAMPORTS_PER_SOL,
  token: "sol",
  network: "devnet",
  });
  ```

  ```python Python lines wrap theme={null}
  from solana.constants import LAMPORTS_PER_SOL

  signature = await sender.transfer(
  to=receiver,
  amount=0.0001 * LAMPORTS_PER_SOL,
  token="sol",
  network="devnet",
  )
  ```
</CodeGroup>

### 3. Wait for transfer result

Finally, wait for the transfer to be confirmed.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  const connection = new Connection("https://api.devnet.solana.com");

  const { blockhash, lastValidBlockHeight } =
  await connection.getLatestBlockhash();

  const confirmation = await connection.confirmTransaction(
  {
  signature,
  blockhash,
  lastValidBlockHeight,
  },
  "confirmed"
  );

  if (confirmation.value.err) {
  console.log(
  `Something went wrong! Error: ${confirmation.value.err.toString()}`
  );
  } else {
  console.log(
  `Transaction confirmed: Link: https://explorer.solana.com/tx/${signature}?cluster=devnet`
  );
  }
  ```

  ```python Python lines wrap theme={null}
  from solana.rpc.api import Client as SolanaClient

  connection = SolanaClient("https://api.devnet.solana.com")

  last_valid_block_height = connection.get_latest_blockhash()

  confirmation = connection.confirm_transaction(
  tx_sig=signature,
  last_valid_block_height=last_valid_block_height.value.last_valid_block_height,
  commitment="confirmed",
  )

  if confirmation.value[0].err:
  print(f"Something went wrong! Error: {confirmation.value.err.toString()}")
  else:
  print(
      f"Transaction confirmed! Link: https://explorer.solana.com/tx/{signature}?cluster=devnet"
  )
  ```
</CodeGroup>

## Complete example

A complete, runnable example can be found below. In the code below, we:

1. Create two EVM EOAs
2. Transfer ETH from one EOA to another
3. Wait for the transfer to be confirmed
4. Create a Smart Account
5. Transfer ETH from the Smart Account to an EOA
6. Wait for the transfer to be confirmed
7. Create two Solana Accounts
8. Transfer SOL from one Solana Account to another
9. Wait for the transfer to be confirmed

<CodeGroup>
  ```ts TypeScript [expandable] lines wrap theme={null}
  import { CdpClient } from '@coinbase/cdp-sdk';
  import { parseEther, createPublicClient, http } from 'viem';
  import { baseSepolia } from 'viem/chains';
  import { Connection } from '@solana/web3.js';

  const publicClient = createPublicClient({
  chain: baseSepolia,
  transport: http(),
  });

  const connection = new Connection("https://api.devnet.solana.com");

  async function sendTransferWithEVMAccount(cdp: CdpClient): Promise<void> {
  console.log("\n=== EOA Example ===");
  const sender = await cdp.evm.getOrCreateAccount({ name: "Sender" });
  const receiver = await cdp.evm.getOrCreateAccount({ name: "Receiver" });

  console.log(`Transferring 0.00001 ETH from ${sender.address} to ${receiver.address}...`);
  const { transactionHash } = await sender.transfer({
  to: receiver,
  amount: parseEther("0.00001"),
  token: "eth",
  network: "base-sepolia"
  });

  const receipt = await publicClient.waitForTransactionReceipt({
  hash: transactionHash,
  });

  console.log(`Transfer status: ${receipt.status}`);
  console.log(
  `Explorer link: https://sepolia.basescan.org/tx/${receipt.transactionHash}`
  );
  }

  async function sendTransferWithSmartAccount(cdp: CdpClient): Promise<void> {
  console.log("\n=== Smart Account Example ===");
  const sender = await cdp.evm.createSmartAccount({
  owner: await cdp.evm.getOrCreateAccount({ name: "Owner" })
  });

  const receiver = await cdp.evm.getOrCreateAccount({ name: "Receiver" });

  console.log(`Transferring 0.00001 ETH from ${sender.address} to ${receiver.address}...`);
  const { userOpHash } = await sender.transfer({
  to: receiver,
  amount: parseEther("0.00001"),
  token: "eth",
  network: "base-sepolia"
  });

  const receipt = await sender.waitForUserOperation({
  userOpHash,
  });

  console.log(`Transfer status: ${receipt.status}`);
  console.log(`Explorer link: https://sepolia.basescan.org/tx/${transactionHash}`);
  }

  async function sendTransferWithSolanaAccount(cdp: CdpClient): Promise<void> {
  console.log("\n=== Solana Account Example ===");
  const sender = await cdp.solana.getOrCreateAccount({ name: "Sender" });
  const receiver = await cdp.solana.getOrCreateAccount({ name: "Receiver" });

  console.log(`Transferring 0.0001 SOL from ${sender.address} to ${receiver.address}...`);
  const { signature } = await sender.transfer({
  to: receiver,
  amount: 0.0001 * LAMPORTS_PER_SOL,
  token: "sol",
  network: "devnet",
  });

  const { blockhash, lastValidBlockHeight } =
  await connection.getLatestBlockhash();

  const confirmation = await connection.confirmTransaction(
  {
    signature,
    blockhash,
    lastValidBlockHeight,
  },
  "confirmed"
  );

  if (confirmation.value.err) {
  console.log(`Something went wrong! Error: ${confirmation.value.err.toString()}`);
  } else {
  console.log(
    `Transaction confirmed: Link: https://explorer.solana.com/tx/${signature}?cluster=devnet`
  );
  }
  }

  async function main(): Promise<void> {
  const cdp = new CdpClient();

  try {
  await sendTransferWithEVMAccount(cdp);
  await sendTransferWithSmartAccount(cdp);
  await sendTransferWithSolanaAccount(cdp);
  } catch (error) {
  console.error('Error:', error);
  }
  }

  if (require.main === module) {
  main().catch(console.error);
  }
  ```

  ```python Python [expandable] lines wrap theme={null}
  import asyncio
  import os
  from cdp import CdpClient
  from solana.rpc.api import Client as SolanaClient
  from web3 import Web3

  w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))

  solana_client = SolanaClient("https://api.devnet.solana.com")

  async def send_transfer_with_EVM_account(cdp):
  print("\n=== EOA Example ===")
  sender = await cdp.evm.get_or_create_account(name="Sender")
  receiver = await cdp.evm.get_or_create_account(name="Receiver")

  print(f"Transferring 0.00001 ETH from {sender.address} to {receiver.address}...")
  tx_hash = await sender.transfer(
      to=receiver,
      amount=Web3.toWei("0.00001", "ether"),
      token="eth",
      network="base-sepolia"
  )

  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

  print(f"Transfer status: {receipt.status}")
  print(f"Explorer link: https://sepolia.basescan.org/tx/{transfer_result.transaction_hash}")

  async def send_transfer_with_smart_account(cdp):
  print("\n=== Smart Account Example ===")
  owner = await cdp.evm.get_or_create_account(name="Owner")
  sender = await cdp.evm.create_smart_account(owner=owner)
  receiver = await cdp.evm.get_or_create_account(name="Receiver")

  print(f"Transferring 0.00001 ETH from {sender.address} to {receiver.address}...")
  transfer_result = await sender.transfer(
      to=receiver,
      amount=Web3.toWei("0.00001", "ether"),
      token="eth",
      network="base-sepolia"
  )

  user_op_result = await sender.wait_for_user_operation(
      user_op_hash=transfer_result.user_op_hash
  )
  print(f"Transfer status: {user_op_result.status}")
  print(f"Explorer link: https://sepolia.basescan.org/tx/{user_op_result.transaction_hash}")

  async def send_transfer_with_solana_account(cdp):
  print("\n=== Solana Account Example ===")
  sender = await cdp.solana.get_or_create_account(name="Sender")
  receiver = await cdp.solana.get_or_create_account(name="Receiver")

  print(f"Transferring 0.0001 SOL from {sender.address} to {receiver.address}...")
  signature = await sender.transfer(
      to=receiver,
      amount=0.0001 * LAMPORTS_PER_SOL,
      token="sol",
      network="devnet",
  )

  last_valid_block_height = solana_client.get_latest_blockhash()

  confirmation = solana_client.confirm_transaction(
      tx_sig=signature,
      last_valid_block_height=last_valid_block_height.value.last_valid_block_height,
      commitment="confirmed",
  )

  if confirmation.value[0].err:
      print(f"Something went wrong! Error: {confirmation.value.err.toString()}")
  else:
      print(
          f"Transaction confirmed! Link: https://explorer.solana.com/tx/{signature}?cluster=devnet"
      )

  async def main():
  async with CdpClient(
      api_key_id = os.getenv("CDP_API_KEY_ID"),
      api_key_secret = os.getenv("CDP_API_KEY_SECRET"),
      wallet_secret = os.getenv("CDP_WALLET_SECRET")
  ) as cdp:
      await send_transfer_with_EVM_account(cdp)
      await send_transfer_with_smart_account(cdp)
      await send_transfer_with_solana_account(cdp)

  if __name__ == "__main__":
  asyncio.run(main())
  ```
</CodeGroup>

After running the complete example, you should see the following:

```console lines wrap theme={null}
=== EOA Example ===
Transferring 0.00001 ETH from 0x689c59617D8Ec93a114E2304cC038bB8678775C7 to 0xe4026d8D0fA814379042f1E245096F0551931d14...
Transfer status: success
Explorer link: https://sepolia.basescan.org/tx/0xdaa53830fb62f407dfe65c6e10bac6c9af1fb2014551d107f7d9de2055914985

=== Smart Account Example ===
Transferring 0.00001 ETH from 0xC3c2D7879B31Aca4e26D16AD57D07422E4a23A67 to 0xe4026d8D0fA814379042f1E245096F0551931d14...
Transfer status: complete
Explorer link: https://sepolia.basescan.org/tx/0x045e29f40897dc01b50a6ba0d7c3d0a424fbca69792869f56e1321f1a899419f

=== Solana Account Example ===
Transferring 0.0001 SOL from DYjMQTJCcqmtdMvagJvW17U7teg8caUQ92nSrcXdqSZG to 32gPVc5gDvn2T5EgV81NFavDMpf5HU4oLUbmuipKpV8C...
Transaction confirmed! Link: https://explorer.solana.com/tx/4KEPbhkRLTg2FJNqV5bbUd6zv1TNkksxF9PDHw2FodrTha3jq2Cojn4hSKtjPWdrZiRDuYp7okRuc1oYvh3JkLuE?cluster=devnet
```

## Transferring ERC-20 Tokens or SPL Tokens

In the examples above, we transferred native tokens (`eth` and `sol`). Using the `transfer` method, you can also easily transfer ERC-20 tokens or SPL tokens, like USDC.
The `transfer` method itself can receive `usdc` as the value for the `token` parameter:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  await sender.transfer({
  to: receiver,
  amount: 10000n, // equivalent to 0.01 USDC
  token: "usdc",
  network: "base-sepolia"
  })
  ```

  ```python Python lines wrap theme={null}
  await sender.transfer(
  to=receiver,
  amount=10000, # equivalent to 0.01 USDC
  token="usdc",
  network="base-sepolia"
  )
  ```
</CodeGroup>

Notice the value passed to the `amount` parameter is specified as `10000` for USDC. This is because USDC has 6 decimal places, so `10000` is equivalent to `0.01 USDC`.
To work with more human-readable values, you can use the `parseUnits` function from `viem` if using TypeScript, or CDP's `parse_units` function if using Python:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { parseUnits } from "viem";

  await sender.transfer({
  to: receiver,
  amount: parseUnits("0.01", 6), // equivalent to 10000n
  token: "usdc",
  network: "base-sepolia"
  })
  ```

  ```python Python lines wrap     theme={null}
  from cdp import parse_units

  await sender.transfer(
  to=receiver,
  amount=parse_units("0.01", 6), # equivalent to 10000
  token="usdc",
  network="base-sepolia"
  )
  ```
</CodeGroup>

The `transfer` method can also receive an arbitrary token contract address as the value for the `token` parameter:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  await sender.transfer({
  to: receiver,
  amount: parseEther("0.00001"),
  token: "0x4200000000000000000000000000000000000006", // Contract address of WETH on Base Sepolia
  network: "base-sepolia"
  })
  ```

  ```python Python lines wrap theme={null}
  await sender.transfer(
  to=receiver,
  amount=Web3.toWei("0.00001", "ether"),
  token="0x4200000000000000000000000000000000000006", # Contract address of WETH on Base Sepolia
  network="base-sepolia"
  )
  ```
</CodeGroup>

## Video: Watch and learn

**Watch this video for a walkthrough of the transfer process:**

<Frame>
  <iframe title="Transfer Process Walkthrough" />
</Frame>

## What to read next

* [Managing Accounts](/server-wallets/v2/using-the-wallet-api/managing-accounts): Learn tips and best practices for managing your accounts
* [Accounts](/server-wallets/v2/introduction/accounts): More information on the different types of accounts available using the v2 Server Wallet

