# Token Balances
Source: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/token-balances



## Overview

With CDP API and SDKs, you can retrieve token balances for any address on supported EVM networks and Solana. This allows you to check balances for both native tokens (like ETH, SOL) and ERC-20/SPL tokens across multiple blockchain networks.

The token balance APIs support querying balances for:

* **EVM Networks**: Ethereum, Base, and Base Sepolia
* **Solana Networks**: Solana Mainnet and Solana Devnet

<Info>
  Token balance queries are **read-only operations** and do not require account ownership. You can check balances for any public address.
</Info>

## EVM Token Balances

Use the `listTokenBalances` method to retrieve token balances for any EVM address. This method returns both native tokens (like ETH) and ERC-20 tokens held by the address.

### Basic Usage

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import "dotenv/config";

  const cdp = new CdpClient();

  const result = await cdp.evm.listTokenBalances({
    address: "0x5b76f5B8fc9D700624F78208132f91AD4e61a1f0",
    network: "base-sepolia",
  });

  console.log(`Found ${result.balances.length} token balances:`);
  for (const balance of result.balances) {
    console.log("Token contract address:", balance.token.contractAddress);
    console.log("Balance amount:", balance.amount.amount);
    console.log("Balance decimals:", balance.amount.decimals);
    console.log("---");
  }
  ```

  ```python Python lines wrap theme={null}
  import asyncio
  from cdp import CdpClient
  from dotenv import load_dotenv

  load_dotenv()

  async def main():
      async with CdpClient() as cdp:
          token_balances = await cdp.evm.list_token_balances(
              address="0x5b76f5B8fc9D700624F78208132f91AD4e61a1f0",
              network="base-sepolia",
          )

          print(f"Found {len(result.balances)} token balances:")
          for balance in token_balances.balances:
              print(f"Token contract address: {balance.token.contract_address}")
              print(f"Balance amount: {balance.amount.amount}")
              print(f"Balance decimals: {balance.amount.decimals}")
              print("---")

  asyncio.run(main())
  ```
</CodeGroup>

### Supported Networks

The EVM token balance API supports the following networks:

* **Mainnet**: `ethereum`, `base`
* **Testnet**: `base-sepolia`

### Pagination

For addresses with many token balances, you can use pagination to retrieve results in manageable chunks:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  // Get the first page of token balances
  const firstPage = await cdp.evm.listTokenBalances({
    address: "0x5b76f5B8fc9D700624F78208132f91AD4e61a1f0",
    network: "base-sepolia",
    pageSize: 10,
  });

  console.log("First page results:");
  for (const balance of firstPage.balances) {
    console.log("Token contract address:", balance.token.contractAddress);
    console.log("Balance amount:", balance.amount.amount);
    console.log("Balance decimals:", balance.amount.decimals);
    console.log("---");
  }

  // Get the next page if available
  if (firstPage.nextPageToken) {
    const secondPage = await cdp.evm.listTokenBalances({
      address: "0x5b76f5B8fc9D700624F78208132f91AD4e61a1f0",
      network: "base-sepolia",
      pageSize: 10,
      pageToken: firstPage.nextPageToken,
    });

    console.log("\nSecond page results:");
    for (const balance of secondPage.balances) {
      console.log("Token contract address:", balance.token.contractAddress);
      console.log("Balance amount:", balance.amount.amount);
      console.log("Balance decimals:", balance.amount.decimals);
      console.log("---");
    }
  }
  ```

  ```python Python lines wrap theme={null}
  # Get the first page of token balances
  first_page = await cdp.evm.list_token_balances(
      address="0x5b76f5B8fc9D700624F78208132f91AD4e61a1f0",
      network="base-sepolia",
      page_size=10,
  )

  print("First page results:")
  for balance in first_page.balances:
      print(f"Token contract address: {balance.token.contract_address}")
      print(f"Balance amount: {balance.amount.amount}")
      print(f"Balance decimals: {balance.amount.decimals}")
      print("---")

  # Get the next page if available
  if first_page.next_page_token:
      second_page = await cdp.evm.list_token_balances(
          address="0x5b76f5B8fc9D700624F78208132f91AD4e61a1f0",
          network="base-sepolia",
          page_size=10,
          page_token=first_page.next_page_token,
      )

      print("\nSecond page results:")
      for balance in second_page.balances:
          print(f"Token contract address: {balance.token.contract_address}")
          print(f"Balance amount: {balance.amount.amount}")
          print(f"Balance decimals: {balance.amount.decimals}")
          print("---")
  ```
</CodeGroup>

## Solana Token Balances

Use the `listTokenBalances` method to retrieve token balances for any Solana address. This method returns both native SOL and SPL tokens held by the address.

### Basic Usage

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import "dotenv/config";

  const cdp = new CdpClient();

  const result = await cdp.solana.listTokenBalances({
    address: "4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK",
    network: "solana-devnet",
  });

  console.log(`Found ${result.balances.length} token balances:`);
  for (const balance of result.balances) {
    console.log("Token mint address:", balance.token.mintAddress);
    console.log("Balance amount:", balance.amount.amount);
    console.log("Balance decimals:", balance.amount.decimals);
    console.log("---");
  }
  ```

  ```python Python lines wrap theme={null}
  import asyncio
  from cdp import CdpClient
  from dotenv import load_dotenv

  load_dotenv()


  async def main():
      async with CdpClient() as cdp:
          result = await cdp.solana.list_token_balances(
              address="4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK",
              network="solana-devnet",
          )

          print(f"Found {len(result.balances)} token balances:")
          for balance in result.balances:
              print("Token mint address:", balance.token.mint_address)
              print("Balance amount:", balance.amount.amount)
              print("Balance decimals:", balance.amount.decimals)
              print("---")
  ```
</CodeGroup>

### Supported Networks

The Solana token balance API supports the following networks:

* **Mainnet**: `solana`
* **Devnet**: `solana-devnet`

### Pagination

For addresses with many token balances, you can use pagination:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  // Get the first page of token balances
  const firstPage = await cdp.solana.listTokenBalances({
    address: "4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK",
    network: "solana-devnet",
    pageSize: 3,
  });

  console.log("First page:");
  for (const balance of firstPage.balances) {
    console.log("Token mint address:", balance.token.mintAddress);
    console.log("Balance amount:", balance.amount.amount);
    console.log("Balance decimals:", balance.amount.decimals);
    console.log("---");
  }

  // Get the next page if available
  if (firstPage.nextPageToken) {
    const secondPage = await cdp.solana.listTokenBalances({
      address: "4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK",
      network: "solana-devnet",
      pageSize: 2,
      pageToken: firstPage.nextPageToken,
    });

    console.log("\nSecond page:");
    for (const balance of secondPage.balances) {
      console.log("Token mint address:", balance.token.mintAddress);
      console.log("Balance amount:", balance.amount.amount);
      console.log("Balance decimals:", balance.amount.decimals);
      console.log("---");
    }
  }
  ```

  ```python Python lines wrap theme={null}

  # Get the first page of token balances
  first_page = await cdp.solana.list_token_balances(
      address="4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK",
      network="solana-devnet",
      page_size=3,
  )

  print("First page:")
  for balance in first_page.balances:
      print("Token mint address:", balance.token.mint_address)
      print("Balance amount:", balance.amount.amount)
      print("Balance decimals:", balance.amount.decimals)
      print("---")

  # Get the next page if available
  if first_page.next_page_token:
      second_page = await cdp.solana.list_token_balances(
          address="4PkiqJkUvxr9P8C1UsMqGN8NJsUcep9GahDRLfmeu8UK",
          network="solana-devnet",
          page_size=2,
          page_token=first_page.next_page_token,
      )

      print("\nSecond page:")
      for balance in second_page.balances:
          print("Token mint address:", balance.token.mint_address)
          print("Balance amount:", balance.amount.amount)
          print("Balance decimals:", balance.amount.decimals)
          print("---")
  ```
</CodeGroup>

## Working with Your Own Accounts

If you want to check balances for accounts you've created with the CDP SDK, you can easily get the address from your account object:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  // Create or get an existing account
  const account = await cdp.evm.getOrCreateAccount({ name: "my-account" });

  // Check the account's token balances
  const balances = await cdp.evm.listTokenBalances({
      address: account.address,
      network: "base-sepolia",
  });
  ```

  ```python Python lines wrap theme={null}
  # Create or get an existing account
  account = await cdp.evm.get_or_create_account(name="my-account")

  # Check the account's token balances
  balances = await cdp.evm.list_token_balances(
      address=account.address,
      network="base-sepolia",
  )
  ```
</CodeGroup>

## Response Format

The token balance response includes detailed information about each token:

### EVM Token Balance Response

```json theme={null}
{
  "balances": [
    {
      "token": {
        "contractAddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "network": "ethereum",
        "symbol": "USDC",
        "name": "USDC",
      },
      "amount": {
        "amount": 1000000,
        "decimals": 6
      }
    }
  ],
  "nextPageToken": "..."
}
```

### Solana Token Balance Response

```json theme={null}
{
  "balances": [
    {
      "token": {
        "mintAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "symbol": "USDC",
        "name": "USDC",
      },
      "amount": {
        "amount": 1000000,
        "decimals": 6
      }
    }
  ],
  "nextPageToken": "..."
}
```

## What to read next

* [Managing Accounts](/server-wallets/v2/using-the-wallet-api/managing-accounts): Learn tips and best practices for managing your accounts
* [API Reference](/api-reference/v2/introduction): Full API reference for the v2 Server Wallet

