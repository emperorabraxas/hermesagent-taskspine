# Trade API: Quickstart
Source: https://docs.cdp.coinbase.com/trade-api/quickstart



## Overview

An onchain trade (otherwise known as a swap) is a transaction that exchanges one token for another.

In this guide, you will learn how to:

* Estimate a swap price
* Execute a swap with regular accounts (EOAs) or Smart Accounts

<Note>
  The Beta launch of our Trade API supports Ethereum, Base, Arbitrum, Optimism and Polygon mainnet networks only - stay tuned for additional network support!
</Note>

### Price estimation

The SDK provides two methods for estimating swap prices:

| Method         | Use Case                                       | Function                                            |
| -------------- | ---------------------------------------------- | --------------------------------------------------- |
| Quick estimate | UI displays, real-time rates, liquidity checks | - `getSwapPrice` (Ts)<br /> - `get_swap_price` (Py) |
| Swap quote     | Pre-execution, approvals, custom handling      | - `quoteSwap` (Ts)<br /> - `quote_swap` (Py)        |

### CDP vs. external libraries

You can execute swaps using either:

1. **CDP Wallet Integration** (Recommended for most use cases)
   * Use our managed wallet infrastructure
   * Automatic transaction signing and submission
   * Built-in security and compliance features
   * **Smart Account support** with gas sponsorship via paymasters
   * See the [Server Wallet v2](/server-wallets/v2/introduction/quickstart) guide for details on setup and the [Server Wallet Swaps guide](/server-wallets/v2/evm-features/swaps) for more information on executing swaps

2. **External Library Integration** (For custom infrastructure)
   * Use libraries like [viem](https://viem.sh) or [web3.py](https://pypi.org/project/web3)
   * Full control over transaction signing
   * Support for custom wallet types (including Smart Accounts with additional setup)
   * Continue reading below for examples

Both options include built-in [slippage](/trade-api/quickstart#slippage) protection to ensure your swap executes at a fair price, even in volatile market conditions. Gas fees are automatically calculated and optimized for the most cost-effective route.

### Slippage

Slippage is the difference between the expected price of a trade and the actual price at which it executes.

<Accordion title="More on slippage protection">
  In these examples, we set a 1% slippage tolerance (using `slippageBps: 100` in TypeScript or `slippage_bps: 100` in Python), meaning the trade will only execute if the final price is within 1% of the expected price.

  This **protects** you from unfavorable trades if the price moves significantly between when you submit the transaction and when it's executed.
</Accordion>

## Prerequisites

It is assumed you have:

* [Node.js](https://nodejs.org/en) 22.x+ if using Typescript
* [Python](https://www.python.org/downloads/) 3.10+ if using Python
* [Created](https://portal.cdp.coinbase.com/create-account) and [signed in](https://portal.cdp.coinbase.com/signin) to an existing CDP account
* Created the necessary keys to authenticate requests (see the [prerequisites](/server-wallets/v2/introduction/quickstart#prerequisites) section in v2 Server Wallet for setup instructions)
* (Optional) For Smart Accounts: Understanding of [account abstraction (ERC-4337)](https://eips.ethereum.org/EIPS/eip-4337) concepts

## Regular Accounts (EOAs)

### 1. Estimate a swap price

To begin, let's walk through an example of how to estimate a swap price with a regular account (EOA).

<Note>
  `getSwapPrice` for Typescript and `get_swap_price` for Python provide estimates only and do not reserve funds. They are suitable for frequent price updates but may be less precise than creating a swap quote.
</Note>

<CodeGroup>
  ```typescript main.ts theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";

  const cdp = new CdpClient();

  // Get price for swapping 1 WETH to USDC on Base
  const swapPrice = await cdp.evm.getSwapPrice({
    fromToken: "0x4200000000000000000000000000000000000006",  // WETH
    toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC
    fromAmount: BigInt("1000000000000000000"),  // 1 WETH (18 decimals)
    network: "base",
    taker: "0x1234567890123456789012345678901234567890"  // Your EOA address
  });

  if (swapPrice.liquidityAvailable) {
    console.log(`You'll receive: ${swapPrice.toAmount} USDC`);
    console.log(`Minimum after slippage: ${swapPrice.minToAmount} USDC`);
  }
  ```

  ```python main.py theme={null}
  from cdp import CdpClient

  async with CdpClient() as cdp:
      # Get price for swapping 100 USDC to WETH on Base
      swap_price = await cdp.evm.get_swap_price(
          from_token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC
          to_token="0x4200000000000000000000000000000000000006",     # WETH
          from_amount="100000000",  # 100 USDC (6 decimals)
          network="base",
          taker="0x1234567890123456789012345678901234567890"  # Your EOA address
      )
      
      if swap_price.liquidity_available:
          print(f"You'll receive: {swap_price.to_amount} WETH")
          print(f"Minimum after slippage: {swap_price.min_to_amount} WETH")
  ```
</CodeGroup>

📖 **Full examples**: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/swaps/getSwapPrice.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/swaps/get_swap_price.py)

### 2. Create a swap quote

Once you're ready to commit to a swap, you can create a swap quote using the CDP API. This gives you the transaction data needed for execution as opposed to the quick price estimate that we demonstrated above.

<Info>
  Creating a swap quote may reserve funds onchain. This action is strictly rate-limited.
</Info>

<CodeGroup>
  ```typescript main.ts theme={null}
  // Using a CDP account
  const account = await cdp.evm.getOrCreateAccount({ name: "MyAccount" });

  // Create a swap quote
  const swapQuote = await account.quoteSwap({
    network: "base",
    toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC
    fromToken: "0x4200000000000000000000000000000000000006",  // WETH
    fromAmount: BigInt("1000000000000000000"),  // 1 WETH (18 decimals)
    slippageBps: 100,  // 1% slippage tolerance
  });

  if (swapQuote.liquidityAvailable) {
    console.log(`Expected output: ${swapQuote.toAmount} USDC`);
    console.log(`Minimum output: ${swapQuote.minToAmount} USDC`);
  }
  ```

  ```python main.py theme={null}
  # Using a CDP account
  account = await cdp.evm.get_or_create_account(name="MyAccount")

  # Create a swap quote
  swap_quote = await account.quote_swap(
      sell_token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC
      buy_token="0x4200000000000000000000000000000000000006",   # WETH
      sell_amount="100000000",  # 100 USDC (6 decimals)
      network="base",
      slippage_bps=100,  # 1% slippage tolerance
  )

  # Check if liquidity is available
  if swap_quote.liquidity_available:
      print(f"Expected output: {swap_quote.buy_amount} WETH")
      print(f"Minimum output: {swap_quote.min_buy_amount} WETH")
  ```
</CodeGroup>

📖 **Full examples**: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/swaps/account.quoteSwap.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/swaps/account.quote_swap.py)

### 3. Execute a swap

Now that we have a swap quote, we can execute it onchain. The easiest way to do this is by using CDP Wallets.

We also offer a smoother developer experience using our Server Wallet. Read the [Server Wallet Swaps guide](/server-wallets/v2/evm-features/swaps) for more information.

<CodeGroup>
  ```typescript main.ts theme={null}
  // Execute the swap using the CDP account (recommended)
  const { transactionHash } = await swapQuote.execute();

  console.log(`Swap executed: ${transactionHash}`);
  ```

  ```python main.py theme={null}
  # Execute the swap using the CDP account (recommended)
  transaction_hash = await swap_quote.execute()

  print(f"Swap executed: {transaction_hash}")
  ```
</CodeGroup>

<Tip>
  **All-in-one swap**

  You can also create and execute a swap in a single call using `account.swap()`:

  <CodeGroup>
    ```typescript main.ts theme={null}
    // Create and execute swap in one call
    const result = await account.swap({
      network: "base",
      toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC
      fromToken: "0x4200000000000000000000000000000000000006",  // WETH
      fromAmount: BigInt("1000000000000000000"),  // 1 WETH
      slippageBps: 100,  // 1% slippage tolerance
    });

    console.log(`Swap executed: ${result.transactionHash}`);
    console.log(`Received: ${result.toAmount} USDC`);
    ```

    ```python main.py theme={null}
    # Create and execute swap in one call
    result = await account.swap({
        "sell_token": "0x4200000000000000000000000000000000000006",  # WETH
        "buy_token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",   # USDC
        "sell_amount": "1000000000000000000",  # 1 WETH
        "network": "base",
        "slippage_bps": 100  # 1% slippage
    })

    print(f"Swap executed: {result.transaction_hash}")
    print(f"Received: {result.to_amount} USDC")
    ```
  </CodeGroup>
</Tip>

📖 **Full examples**:

* Quote & Execute: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/swaps/account.quoteSwapAndExecute.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/swaps/account.quote_swap_and_execute.py)
* All-in-one: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/swaps/account.swap.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/swaps/account.swap.py)

## Smart Accounts

Smart Accounts provide additional features like gas sponsorship and batch operations. The key differences are:

* Use the Smart Account address (not the owner's EOA) as the `taker`
* Transactions return `userOpHash` instead of `transactionHash`
* Must wait for user operations to complete

### 1. Estimate a swap price

When estimating prices for Smart Accounts, use the Smart Account address as the `taker`:

<CodeGroup>
  ```typescript main.ts theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";

  const cdp = new CdpClient();

  // First, create or get your Smart Account
  const owner = await cdp.evm.getOrCreateAccount({ name: "OwnerAccount" });
  const smartAccount = await cdp.evm.getOrCreateSmartAccount({ 
    name: "MySmartAccount",
    owner: owner
  });

  // Get price using the Smart Account address
  const swapPrice = await cdp.evm.getSwapPrice({
    fromToken: "0x4200000000000000000000000000000000000006",  // WETH
    toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC
    fromAmount: BigInt("1000000000000000000"),  // 1 WETH (18 decimals)
    network: "base",
    taker: smartAccount.address  // Smart Account address, not owner EOA
  });

  if (swapPrice.liquidityAvailable) {
    console.log(`You'll receive: ${swapPrice.toAmount} USDC`);
    console.log(`Minimum after slippage: ${swapPrice.minToAmount} USDC`);
  }
  ```

  ```python main.py theme={null}
  from cdp import CdpClient

  async with CdpClient() as cdp:
      # First, create or get your Smart Account
      owner = await cdp.evm.get_or_create_account(name="OwnerAccount")
      smart_account = await cdp.evm.get_or_create_smart_account(
          name="MySmartAccount",
          owner=owner
      )
      
      # Get price using the Smart Account address
      swap_price = await cdp.evm.get_swap_price(
          from_token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC
          to_token="0x4200000000000000000000000000000000000006",     # WETH
          from_amount="100000000",  # 100 USDC (6 decimals)
          network="base",
          taker=smart_account.address  # Smart Account address, not owner EOA
      )
      
      if swap_price.liquidity_available:
          print(f"You'll receive: {swap_price.to_amount} WETH")
          print(f"Minimum after slippage: {swap_price.min_to_amount} WETH")
  ```
</CodeGroup>

📖 **Full examples**: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/swaps/getSwapPrice.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/swaps/get_swap_price.py)

### 2. Create a swap quote

Once you're ready to commit to a swap, you can create a swap quote using the CDP API. This gives you the transaction data needed for execution as opposed to the quick price estimate that we demonstrated above.

<Info>
  Creating a swap quote may reserve funds onchain. This action is strictly rate-limited.
</Info>

<CodeGroup>
  ```typescript main.ts theme={null}
  // Create a swap quote with Smart Account
  const swapQuote = await smartAccount.quoteSwap({
    network: "base",
    toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC
    fromToken: "0x4200000000000000000000000000000000000006",  // WETH
    fromAmount: BigInt("1000000000000000000"),  // 1 WETH (18 decimals)
    slippageBps: 100,  // 1% slippage tolerance
    // paymasterUrl: "https://your-paymaster.com" // Optional: sponsor gas fees
  });

  // Check if liquidity is available
  if (swapQuote.liquidityAvailable) {
    console.log(`Expected output: ${swapQuote.toAmount} USDC`);
    console.log(`Minimum output: ${swapQuote.minToAmount} USDC`);
  }
  ```

  ```python main.py theme={null}
  # Create a swap quote with Smart Account
  swap_quote = await smart_account.quote_swap(
      sell_token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC
      buy_token="0x4200000000000000000000000000000000000006",   # WETH
      sell_amount="100000000",  # 100 USDC (6 decimals)
      network="base",
      slippage_bps=100,  # 1% slippage tolerance
      # paymaster_url="https://your-paymaster.com"  # Optional: sponsor gas fees
  )

  # Check if liquidity is available
  if not swap_quote.liquidity_available:
      print(f"Expected output: {swap_quote.buy_amount} WETH")
      print(f"Minimum output: {swap_quote.min_buy_amount} WETH")
  ```
</CodeGroup>

📖 **Full examples**: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/smart-accounts/smartAccount.quoteSwap.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/smart-accounts/smart_account.quote_swap.py)

### 3. Execute a swap

Now that we have a swap quote, we can execute it onchain. The easiest way to do this is by using CDP Wallets.

Executing swaps with Smart Accounts returns a user operation hash instead of a transaction hash. You must wait for the user operation to complete:

<CodeGroup>
  ```typescript main.ts theme={null}
  // Execute the swap using the Smart Account
  const { userOpHash } = await swapQuote.execute();

  console.log(`User operation submitted: ${userOpHash}`);

  // Wait for the user operation to be mined
  const receipt = await smartAccount.waitForUserOperation({
    userOpHash: userOpHash
  });

  if (receipt.status === "complete") {
    console.log(`Swap completed! Transaction: ${receipt.transactionHash}`);
  } else {
    console.error(`User operation failed: ${receipt.status}`);
  }


  ```

  ```python main.py theme={null}
  # Execute the swap using the Smart Account
  user_op_hash = await swap_quote.execute()

  print(f"User operation submitted: {user_op_hash}")

  # Wait for the user operation to be mined
  receipt = await smart_account.wait_for_user_operation(
      user_op_hash=user_op_hash
  )

  if receipt.status == "complete":
      print(f"Swap completed! Transaction: {receipt.transaction_hash}")
  else:
      print(f"User operation failed: {receipt.status}")


  ```
</CodeGroup>

<Tip>
  **All-in-one swap**

  You can also create and execute a swap in a single call using `smartAccount.swap()`:

  <CodeGroup>
    ```typescript main.ts theme={null}
    // Create and execute swap in one call
    const result = await smartAccount.swap({
      network: "base",
      toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC
      fromToken: "0x4200000000000000000000000000000000000006",  // WETH
      fromAmount: BigInt("1000000000000000000"),  // 1 WETH
      slippageBps: 100,  // 1% slippage tolerance
      // paymasterUrl: "https://your-paymaster.com" // Optional: sponsor gas
    });

    console.log(`User operation submitted: ${result.userOpHash}`);

    // Wait for confirmation
    const receipt = await smartAccount.waitForUserOperation({
      userOpHash: result.userOpHash
    });

    if (receipt.status === "complete") {
      console.log(`Swap completed! Transaction: ${receipt.transactionHash}`);
    }
    ```

    ```python main.py theme={null}
    # Create and execute swap in one call
    result = await smart_account.swap({
        "sell_token": "0x4200000000000000000000000000000000000006",  # WETH
        "buy_token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",   # USDC
        "sell_amount": "1000000000000000000",  # 1 WETH
        "network": "base",
        "slippage_bps": 100,  # 1% slippage
        # "paymaster_url": "https://your-paymaster.com"  # Optional
    })

    print(f"User operation submitted: {result.user_op_hash}")

    # Wait for confirmation
    receipt = await smart_account.wait_for_user_operation(
        user_op_hash=result.user_op_hash
    )

    if receipt.status == "complete":
        print(f"Swap completed! Transaction: {receipt.transaction_hash}")
    ```
  </CodeGroup>
</Tip>

📖 **Full examples**:

* Quote & Execute: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/smart-accounts/smartAccount.quoteSwapAndExecute.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/smart-accounts/smart_account.quote_swap_and_execute.py)
* All-in-one: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/smart-accounts/swap.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/smart-accounts/swap.py)

<Info>
  **Smart Account Benefits**

  * **Gas Sponsorship**: Use paymasters to pay gas fees on behalf of users
  * **Batch Operations**: Combine multiple swaps or operations in one transaction
  * **Account Abstraction**: Enhanced UX with features like session keys and social recovery
  * **Security**: Multi-signature capabilities and spending limits
</Info>

## Using External Wallets

If you prefer to use your own wallet, signing infrastructure, and node for broadcasting transactions, you can use the core Trade APIs (like `getSwapPrice` and `quoteSwap`) without a CDP account.

📖 **Full examples**: [TypeScript](https://github.com/coinbase/cdp-sdk/blob/main/examples/typescript/evm/ecosystem/viem/viem.account.swap.ts) | [Python](https://github.com/coinbase/cdp-sdk/blob/main/examples/python/evm/ecosystem/web3py/web3_account.quote_swap_and_execute.py)

<Note>
  **Custom Wallet Integration**

  If you're using your own wallet infrastructure (e.g., viem, web3.py, etc.), you can execute swaps using the transaction data from the quote. For Smart Accounts with external wallets, additional ERC-4337 infrastructure setup is required.
</Note>

## What to read next

* **[Welcome](/trade-api/welcome#why-use-swap-api-over-aggregator-solutions):** Read why Trade API is easier to use than traditional aggregator solutions.
* **[API Reference](/api-reference/v2/introduction):** Explore the full CDP API v2 documentation.
* **[Server Wallet v2](/server-wallets/v2/introduction/quickstart):** Learn more about our new Server Wallet, including account management and transaction signing.
* **[USDC Rewards](/server-wallets/v2/introduction/usdc-rewards):** Learn how to earn 3.35% rewards on USDC balances in your CDP wallets.

