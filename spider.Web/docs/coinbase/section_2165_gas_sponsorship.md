# Gas Sponsorship
Source: https://docs.cdp.coinbase.com/server-wallets/v2/evm-features/gas-sponsorship



## Overview

Smart Accounts unlock the ability for developers to sponsor gas on their users' transactions.
With the CDP SDK, it's simple to integrate any paymaster URL and cover gas costs for all transactions originating from your smart accounts.

You can refer to this [guide](/paymaster/introduction/welcome) on how to set up a CDP Paymaster. You could also use any provider of your choice.

### Benefits:

* Removes the friction of requiring users to hold ETH
* Enables users to interact with your app immediately
* Provides a more familiar Web2-like experience for new users
* Allows you to subsidize or fully cover transaction costs for your users
* Gives you control over which transactions you want to sponsor

## Prerequisites

* A Coinbase Developer Platform account
* The following environment variables in your `.env` file:

```
CDP_API_KEY_ID=your_api_key_id
CDP_API_KEY_SECRET=your_api_key_secret
CDP_WALLET_SECRET=your_wallet_secret
```

<Tip>
  Navigate to the CDP Portal to find or create your [wallet secret], walletid, and [client api key]
</Tip>

All user operations on Base Sepolia are sponsored by default. For mainnet, you can specify a paymaster of your choice as follows:

<CodeGroup>
  ```ts TypeScript  [expandable] theme={null}
  import dotenv from "dotenv";
  import { parseEther } from "viem";
  import { CdpClient } from "@coinbase/cdp-sdk";

  dotenv.config();

  const cdp = new CdpClient({
    apiKeyId: process.env.CDP_API_KEY_ID,
    apiKeySecret: process.env.CDP_API_KEY_SECRET,
    walletSecret: process.env.CDP_WALLET_SECRET,
  });

  const account = await cdp.evm.createAccount();

  const smartAccount = await cdp.evm.createSmartAccount({
    owner: account,
  });

  const userOperation = await cdp.evm.sendUserOperation({
    smartAccount: smartAccount,
    network: "base-sepolia",
    calls: [
      {
        to: "0x0000000000000000000000000000000000000000",
        value: parseEther("0"),
        data: "0x",
      },
    ],
    paymasterUrl: "https://some-paymaster-url.com",
  });

  console.log("User Operation Result:", userOperation);
  ```

  ```python Python  [expandable] theme={null}
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
              network="base",
              paymaster_url="https://some-paymaster-url.com",
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

You can apply for [gas credits](https://docs.google.com/forms/d/1yPnBFW0bVUNLUN_w3ctCqYM9sjdIQO3Typ53KXlsS5g/viewform?edit_requested=true\&pli=1) as you scale.

## Gas sponsorship with EIP-7702 delegated accounts

If you're using [EIP-7702 delegation](/server-wallets/v2/evm-features/eip-7702-delegation) to upgrade an existing EOA with smart account capabilities, gas sponsorship works the same way — pass a `paymasterUrl` to `sendUserOperation` on the delegated account.

<Note>
  The account must have completed EIP-7702 delegation before sending user operations. See the [EIP-7702 Delegation guide](/server-wallets/v2/evm-features/eip-7702-delegation) for the full delegation flow.
</Note>

<CodeGroup>
  ```ts TypeScript  [expandable] theme={null}
  import { CdpClient, toEvmDelegatedAccount } from "@coinbase/cdp-sdk";
  import { parseEther } from "viem";
  import dotenv from "dotenv";

  dotenv.config();

  const cdp = new CdpClient();

  // Retrieve the account that has already been delegated
  const account = await cdp.evm.getOrCreateAccount({ name: "My-EIP7702-Account" });

  const delegatedAccount = toEvmDelegatedAccount(account);

  const { userOpHash } = await delegatedAccount.sendUserOperation({
    network: "base-sepolia",
    calls: [
      {
        to: "0x0000000000000000000000000000000000000000",
        value: parseEther("0"),
        data: "0x",
      },
    ],
    paymasterUrl: "https://some-paymaster-url.com",
  });

  console.log("User operation submitted:", userOpHash);
  ```

  ```python Python  [expandable] theme={null}
  import asyncio
  from cdp import CdpClient, to_evm_delegated_account
  from cdp.evm_call_types import EncodedCall
  from dotenv import load_dotenv

  load_dotenv()

  async def main():
      async with CdpClient() as cdp:
          # Retrieve the account that has already been delegated
          account = await cdp.evm.get_or_create_account(name="My-EIP7702-Account")

          delegated = to_evm_delegated_account(account)

          user_op = await delegated.send_user_operation(
              calls=[
                  EncodedCall(
                      to="0x0000000000000000000000000000000000000000",
                      value=0,
                      data="0x",
                  )
              ],
              network="base-sepolia",
              paymaster_url="https://some-paymaster-url.com",
          )

          print(f"User operation submitted: {user_op.user_op_hash}")

  asyncio.run(main())
  ```
</CodeGroup>

## Common Issues

* If transactions fail, verify your gas estimates
* If paymaster fails, check your paymaster client and network configuration
* Make sure your environment variables are properly set in your `.env` file
* Verify you're on the correct network before proceeding with transactions

## Additional Resources

* [Paymaster Documentation](/paymaster/introduction/welcome)
* [Account Abstraction Basics](/paymaster/faqs#basics)
* [Get started with Coinbase Developer Platform](/get-started/quickstart)
* [EIP-7702 Delegation](/server-wallets/v2/evm-features/eip-7702-delegation)

***

[wallet secret]: https://portal.cdp.coinbase.com/products/server-wallets

[client api key]: https://portal.cdp.coinbase.com/projects/api-keys

