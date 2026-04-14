# Token Balances SDK
Source: https://docs.cdp.coinbase.com/data/token-balance/cdp-sdk



## Overview

The CDP SDK allows you to retrieve token balances of an address using the `listTokenBalances` method for Base. For Solana token balances, use the [REST API](/api-reference/v2/rest-api/solana-token-balances/list-solana-token-balances) directly.

Additional information can be found in our [SDK Reference](https://coinbase.github.io/cdp-sdk/typescript/classes/Client.EvmClient.html#listtokenbalances).

In this guide, you will learn how to retrieve ERC-20 and native gas token balances of an address on Base networks.

## Prerequisites

* [Node.js](https://nodejs.org/en/download/) installed
* A free account logged in on [CDP Portal](https://portal.cdp.coinbase.com) and a [Secret API key](https://portal.cdp.coinbase.com/projects/api-keys)

### Configure

<Steps>
  <Step title="Install dependencies">
    ```bash theme={null}
    npm install @coinbase/cdp-sdk dotenv
    ```
  </Step>

  <Step title="Create an .env file">
    Create a `.env` file in your project root:

    ```bash theme={null}
    touch .env
    ```
  </Step>

  <Step title="Add API credentials">
    If you downloaded your CDP API key as a JSON file, it will look like this. Otherwise, you can copy the values directly from the CDP Portal:

    ```json theme={null}
    {
      "id": "3008043e-4528-46b7-82ff-111111111111",
      "privateKey": "a-long-base64-encoded-string"
    }
    ```

    Copy these values into your `.env` file:

    ```bash theme={null}
    CDP_API_KEY_ID=3008043e-4528-46b7-82ff-111111111111
    CDP_API_KEY_SECRET=a-long-base64-encoded-string
    ```
  </Step>
</Steps>

## Example

In the example below, we query token balances for a known exchange address on Base mainnet.

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";
  import "dotenv/config";

  const cdp = new CdpClient();

  // Check token balances for a known exchange wallet with many tokens
  const walletAddress = "0x835678a611b28684005a5e2233695fb6cbbb0007";
  const network = "base";  // Base mainnet

  const result = await cdp.evm.listTokenBalances({
    address: walletAddress,
    network: network,
  });

  console.log(`Checking wallet: ${walletAddress}`);
  console.log(`Network: ${network}\n`);

  result.balances.forEach((item) => {
    // Token amounts are stored as large integers on-chain
    // We divide by 10^decimals to get the human-readable amount
    const readableAmount = Number(item.amount.amount) / Math.pow(10, item.amount.decimals);
    
    // The address 0xEeee... represents native ETH (not an ERC-20 token)
    if (item.token.contractAddress === '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE') {
      console.log(`ETH: ${readableAmount.toFixed(6)}`);
    } else {
      console.log(`Token: ${readableAmount.toFixed(2)} (contract: ${item.token.contractAddress})`);
    }
  });
  ```
</CodeGroup>

After running the snippet above, you should see the following output:

```console theme={null}
Checking wallet: 0x835678a611b28684005a5e2233695fb6cbbb0007
Network: base

Token: 150.00 (contract: 0x1198CabDb2b9fF79EC8CbaFfB8977DAF74AFa25a)
Token: 87331987.01 (contract: 0x6D51bC9d512072B6399B81c73F02ba935B2771e5)
Token: 11000.00 (contract: 0x260b9AC75753FbD67F2Ea6D10724dd89a52C1913)
Token: 1261267.05 (contract: 0x3A95F48Cb4c04Eb0EC2a54d72DAA9e1138D9238d)
Token: 2900.00 (contract: 0x1aD2449781a03197BD6A072598Ac311B8bA1f5BD)
Token: 3086.69 (contract: 0xd6e03dEd9Cf9213b207E69570561E08cc3BC681e)
```

This output shows:

* **Token balances**: Each ERC-20 token with its amount and contract address
* **Contract addresses**: The long hex strings identify each specific token contract on Base mainnet
* **Large holdings**: This exchange wallet holds millions of various tokens

## Sample response

The token balance response provides detailed token information:

```json theme={null}
{
  "balances": [
    {
      "token": {
        "network": "base",
        "symbol": "ETH",
        "name": "Ether",
        "contractAddress": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
      },
      "amount": {
        "amount": "1250000000000000000",
        "decimals": 18
      }
    }
  ],
  "nextPageToken": "..."
}
```

### Response fields

| Field             | Description                                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `balances`        | The list of EVM token balances.                                                                                                       |
| `amount`          | Amount of a given token in JSON format, includes `amount`, denominated in the smallest indivisible unit of the token; and `decimals`. |
| `token`           | General information about a token in JSON format.                                                                                     |
| `network`         | Name of the blockchain network, e.g. `base`.                                                                                          |
| `symbol`          | The symbol of the ERC-20 or native gas token, e.g. `ETH`.                                                                             |
| `name`            | The name of the ERC-20 or native gas token, e.g. `Ether`.                                                                             |
| `contractAddress` | Address of the ERC-20 or native gas token smart contract.                                                                             |
| `nextPageToken`   | The token for the next page of items, if any.                                                                                         |

## Pagination

`listTokenBalances` supports paginated responses for addresses with many balances:

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";

  const cdp = new CdpClient();

  const page = await cdp.evm.listTokenBalances({
    address: "0x835678a611b28684005a5e2233695fb6cbbb0007",
    network: "base",
    pageSize: 5
  });

  const nextPage = await cdp.evm.listTokenBalances({
    address: "0x835678a611b28684005a5e2233695fb6cbbb0007",
    network: "base",
    pageToken: page.nextPageToken
  });
  ```

  ```python Python lines wrap theme={null}
  from cdp import CdpClient

  page = await cdp.evm.list_token_balances(
      address="0x835678a611b28684005a5e2233695fb6cbbb0007",
      network="base",
      page_size=5
  )

  next_page = await cdp.evm.list_token_balances(
      address="0x835678a611b28684005a5e2233695fb6cbbb0007",
      network="base",
      page_token=page.next_page_token
  )
  ```
</CodeGroup>

## What to read next

* **[SDK Reference](https://coinbase.github.io/cdp-sdk/typescript/classes/Client.EvmClient.html#listtokenbalances)**: SDK documentation for Base `listTokenBalances`
* **[Base API Reference](/api-reference/v2/rest-api/evm-token-balances/list-evm-token-balances)**: Base REST API endpoint details
* **[Solana API Reference](/api-reference/v2/rest-api/solana-token-balances/list-solana-token-balances)**: Solana REST API endpoint details

