# Using Smart Accounts
Source: https://docs.cdp.coinbase.com/server-wallets/v2/evm-features/smart-accounts



## Overview

[Smart accounts](/server-wallets/v2/introduction/accounts#smart-accounts) are a type of account that can be used to execute user operations onchain.

In this guide, you will learn how to:

* Create an EVM smart account
* Send a user operation from the smart account
* Batch calls within a single user operation

<Note>
  Smart accounts currently have the following limitations:

  * An EVM account can be the owner of only one smart account.
  * A smart account can only have one owner.
  * User operations must be sent sequentially, not concurrently. A single user operation
    can contain multiple calls.
</Note>

## Prerequisites

It is assumed you have already completed the [Quickstart](/server-wallets/v2/introduction/quickstart) guide.

## 1. Create a smart account

An **EVM smart account** is a smart contract account deployed on an EVM compatible network that
provides the ability to batch transactions, sponsor gas, and manage spend permissions.

Smart accounts require an **owner** account to sign on its behalf.

In this example, we will only create the smart account, and use a CDP EVM account as the owner.
Note that the smart contract is not deployed until the following step when you submit the first user operation.

<Note>
  Smart accounts are created with the [`CREATE2`](https://eips.ethereum.org/EIPS/eip-1014) opcode,
  allowing us to access a contract address before it is deployed.

  The actual smart contract is not deployed until the first user operation is submitted.

  Learn more about account abstraction in the [Coinbase Crypto glossary](https://www.coinbase.com/learn/crypto-glossary/what-is-account-abstraction-and-why-is-it-important).
</Note>

<CodeGroup>
  ```ts main.ts lines wrap  theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";
      import dotenv from "dotenv";

      dotenv.config();

      const cdp = new CdpClient();

      const account = await cdp.evm.createAccount();

      const smartAccount = await cdp.evm.createSmartAccount({
        owner: account,
      });

      console.log(
        `Created smart account: ${smartAccount.address}. Owner address: ${account.address}`
      );
  ```

  ```python main.py lines wrap theme={null}
      import asyncio
      from cdp import CdpClient
      import dotenv

      dotenv.load_dotenv()

      async def main():
          cdp = CdpClient()
          
          account = await cdp.evm.create_account()
          smart_account = await cdp.evm.create_smart_account(account)
          print(f"Created smart account: {smart_account.address}")

          await cdp.close()


      asyncio.run(main())
  ```
</CodeGroup>

After running the above snippet, you should see output similar to the following:

```console lines wrap theme={null}
Created smart account: 0x7a3D84055994c3062819Ce8730869D0aDeA4c3Bf
```

## 2. Send a [user operation](https://www.erc4337.io/docs/understanding-ERC-4337/user-operation)

A user operation is a transaction that is executed by a smart account. In this example, we will:

* Create an [externally owned account](/server-wallets/v2/introduction/accounts#externally-owned-accounts)
* Create a smart account with the EOA as the owner
* Submit a user operation on Base Sepolia from the smart account which transfers 0 ETH to the EOA

<Note>
  On Base Sepolia, smart account user operations are subsidized, meaning the smart account does not
  need to be funded with ETH to submit a user operation. On Base mainnet, you will need to fund the smart account
  with ETH before you can submit a user operation.
</Note>

<CodeGroup>
  ```ts main.ts lines wrap [expandable] theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";

      import { parseEther } from "viem";

      import dotenv from "dotenv";

      dotenv.config();

      const cdp = new CdpClient();

      const owner = await cdp.evm.createAccount({});
      console.log("Created owner account:", owner.address);

      const smartAccount = await cdp.evm.createSmartAccount({
        owner,
      });
      console.log("Created smart account:", smartAccount.address);

      const result = await cdp.evm.sendUserOperation({
        smartAccount,
        network: "base-sepolia",
        calls: [
          {
            to: "0x0000000000000000000000000000000000000000",
            value: parseEther("0"),
            data: "0x",
          },
        ],
      });

      console.log("User operation status:", result.status);

      console.log("Waiting for user operation to be confirmed...");
      const userOperation = await cdp.evm.waitForUserOperation({
        smartAccountAddress: smartAccount.address,
        userOpHash: result.userOpHash,
      });

      if (userOperation.status === "complete") {
        console.log("User operation confirmed. Block explorer link:", `https://sepolia.basescan.org/tx/${userOperation.transactionHash}`);
      } else {
        console.log("User operation failed");
      }
  ```

  ```python main.py lines wrap [expandable] theme={null}
      import asyncio
      from decimal import Decimal
      from web3 import Web3
      from cdp import CdpClient
      from cdp.evm_call_types import EncodedCall
      from dotenv import load_dotenv

      load_dotenv()

      async def main():
          cdp = CdpClient()
          
          try:
              # Create EVM account
              account = await cdp.evm.create_account()
              print(f"Created owner account: {account.address}")
              
              # Create smart account with EVM account as owner
              smart_account = await cdp.evm.create_smart_account(account)
              print(f"Created smart account: {smart_account.address}")

              # Send user operation
              user_operation = await cdp.evm.send_user_operation(
                  smart_account=smart_account,
                  calls=[
                      EncodedCall(
                          to=account.address,
                          data="0x",
                          value=Web3.to_wei(Decimal("0"), "ether"),
                      )
                  ],
                  network="base-sepolia",
              )
              print(f"User operation status: {user_operation.status}")

              # Wait for user operation confirmation
              print("Waiting for user operation to be confirmed...")
              user_operation = await cdp.evm.wait_for_user_operation(
                  smart_account_address=smart_account.address,
                  user_op_hash=user_operation.user_op_hash,
              )
              
              if user_operation.status == "complete":
                  print(f"User operation confirmed. Block explorer link: https://basescan.org/tx/{user_operation.transaction_hash}")
              else:
                  print("User operation failed")
          except Exception as e:
              print(f"Error: {e}")
          finally:
              await cdp.close()
              

      asyncio.run(main())
  ```
</CodeGroup>

After running the above snippet, you should see similar output:

````console lines wrap theme={null}
Created owner account: 0x088a49cAf927B8DacEFc4ccFD0D5EAdeC06F19A2
Created smart account: 0x929444AFfd714c260bb6695c921bEB99d1D31ff7
User operation status: broadcast
Waiting for user operation to be confirmed...
User operation confirmed. Block explorer link: https://basescan.org/tx/0x8e66c974c8d1b2a75fee35e097fe9171d28c48066472bb6ed81ca81a10d3c321```
````

## 3. Batch calls within a single user operation

A smart account can batch multiple calls in a single user operation through the `calls` field.

In this example, we will:

* Create an [externally owned account](/server-wallets/v2/introduction/accounts#externally-owned-accounts)
* Create a smart account with the EOA as the owner
* Fund the smart account using a faucet
* Submit a batch transaction with 3 calls

<CodeGroup>
  ```ts main.ts lines wrap [expandable] theme={null}
      import { CdpClient } from "@coinbase/cdp-sdk";

      import { createPublicClient, http, parseEther, Calls } from "viem";
      import { baseSepolia } from "viem/chains";
      import dotenv from "dotenv";

      dotenv.config();

      const cdp = new CdpClient();

      const account = await cdp.evm.createAccount();
      const smartAccount = await cdp.evm.createSmartAccount({ owner: account });
      console.log("Created smart account:", smartAccount.address);

      const { transactionHash } = await smartAccount.requestFaucet({
        network: "base-sepolia",
        token: "eth",
      });

      const publicClient = createPublicClient({
        chain: baseSepolia,
        transport: http(),
      });

      const faucetTxReceipt = await publicClient.waitForTransactionReceipt({
        hash: transactionHash,
      });
      console.log("Faucet transaction confirmed:", faucetTxReceipt.transactionHash);

      const destinationAddresses = [
        "0xba5f3764f0A714EfaEDC00a5297715Fd75A416B7",
        "0xD84523e4F239190E9553ea59D7e109461752EC3E",
        "0xf1F7Bf05A81dBd5ACBc701c04ce79FbC82fEAD8b",
      ];

      const calls = destinationAddresses.map((destinationAddress) => ({
        to: destinationAddress,
        value: parseEther("0.000001"),
        data: "0x",
      }));

      console.log("Sending user operation to three destinations...");
      const { userOpHash } = await smartAccount.sendUserOperation({
        network: "base-sepolia",
        calls: calls as Calls<unknown[]>,
      });

      console.log("Waiting for user operation to be confirmed...");
      const userOperationResult = await smartAccount.waitForUserOperation({
        userOpHash,
      });

      if (userOperationResult.status === "complete") {
        console.log("User operation confirmed. Block explorer link:", `https://sepolia.basescan.org/tx/${userOperationResult.transactionHash}`);
      } else {
        console.log("User operation failed.");
      }
  ```

  ```python main.py lines wrap [expandable] theme={null}
      import asyncio
      from decimal import Decimal
      from web3 import Web3

      from cdp import CdpClient
      from cdp.evm_call_types import EncodedCall
      from dotenv import load_dotenv

      load_dotenv()

      async def main():
          w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))

          # Default destinations and amount
          destinations = [
              "0xba5f3764f0A714EfaEDC00a5297715Fd75A416B7",
              "0xD84523e4F239190E9553ea59D7e109461752EC3E", 
              "0xf1F7Bf05A81dBd5ACBc701c04ce79FbC82fEAD8b"
          ]
          amount = 1000

          async with CdpClient() as cdp:
              # Create new owner and smart account
              account = await cdp.evm.create_account()
              smart_account = await cdp.evm.create_smart_account(account)
              print("Created smart account:", smart_account.address)

              # Always request faucet funds
              faucet_hash = await cdp.evm.request_faucet(
                  address=smart_account.address, network="base-sepolia", token="eth"
              )

              w3.eth.wait_for_transaction_receipt(faucet_hash)
              print(f"Faucet transaction confirmed: {faucet_hash}")

              # Create the user operation with multiple calls in it
              calls = [EncodedCall(
                  to=destination,
                  data="0x",
                  value=Web3.to_wei(Decimal(amount), "wei"),
              ) for destination in destinations]

              print("Sending user operation to three destinations...")
              user_operation = await cdp.evm.send_user_operation(
                  smart_account=smart_account,
                  calls=calls,
                  network="base-sepolia",
              )

              print("Waiting for user operation to be confirmed...")
              user_operation = await cdp.evm.wait_for_user_operation(
                  smart_account_address=smart_account.address,
                  user_op_hash=user_operation.user_op_hash,
              )

              if user_operation.status == "complete":
                  print("User operation confirmed. Block explorer link:", f"https://sepolia.basescan.org/tx/{user_operation.transaction_hash}")
              else:
                  print("User operation failed.")

      asyncio.run(main())
  ```
</CodeGroup>

After running the above snippet, you should see output similar to the following:

```console lines wrap theme={null}
Created smart account: 0xA557E90004ba5406A3553897e99D1FC5A2685F6d
Faucet transaction confirmed: 0xa691fcfd1dcacad1ef144461e9c2f1fc110172f0fcfe9a10cbc83e5ca2b6b610
Sending user operation to three destinations...
Waiting for user operation to be confirmed...
User operation confirmed. Block explorer link: https://sepolia.basescan.org/tx/0xd01b2089fd6d4673eae0d7629bcdf5488ff950dba2b7741b4725632f29e9f1ab
```

## Debugging user operation failure

When a user operation reverts onchain, the reason for the revert is included in its receipt, if it can be decoded.
You can use the SDK to fetch the user operation and inspect its receipt as shown below.

<CodeGroup>
  ```ts main.ts theme={null}
  const userOp = cdp.evm.getUserOperation({
    userOpHash: result.userOpHash,
    smartAccount: smartAccount,
  })

  console.log(userOp.receipts);
  ```

  ```python main.py theme={null}
   user_op = await cdp.evm.get_user_operation(smart_account.address,user_operation.user_op_hash)
   print(user_op.receipts)
  ```
</CodeGroup>

## What to read next

* [**Spend Permissions**](/server-wallets/v2/evm-features/spend-permissions): Learn more about spend permissions
* [**Gas Sponsorship**](/server-wallets/v2/evm-features/gas-sponsorship): Sponsor gas fees for your users' transactions

