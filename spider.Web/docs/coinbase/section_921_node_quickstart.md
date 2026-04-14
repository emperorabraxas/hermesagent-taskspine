# Node Quickstart
Source: https://docs.cdp.coinbase.com/data/node/quickstart



Get started with CDP Node in minutes. This guide shows you how to get your RPC endpoint and make your first blockchain request—both in the browser playground and programmatically in your code.

## Prerequisites

* A free [CDP account](https://portal.cdp.coinbase.com/)

That's it! No complex setup, no infrastructure to manage.

## 1. Try it in the playground

<NodePlaygroundQuickstart />

## 2. Get your RPC endpoint

To use Node in your application, you need an **RPC endpoint URL**. This is the web address where you send blockchain requests—think of it like an API endpoint, but specifically for blockchain operations.

<Steps>
  <Step title="Navigate to Node">
    Go to the [Node page](https://portal.cdp.coinbase.com/products/node) in CDP Portal.
  </Step>

  <Step title="Select your network">
    Choose your target network from the dropdown:

    * **Base Mainnet** - For production applications
    * **Base Sepolia** - For development and testing

    <Frame>
      <img alt="Network selection dropdown in Node configuration" />
    </Frame>
  </Step>

  <Step title="Copy your endpoint URL">
    Copy the displayed RPC endpoint URL. It will look like:

    ```
    https://api.developer.coinbase.com/rpc/v1/base/YOUR_CLIENT_API_KEY
    ```

    The Client API key is automatically included in the URL for authentication.
  </Step>
</Steps>

<Info>
  **About Client API Keys**

  Your RPC endpoint URL includes a Client API key, which is designed for client-side use and is safe to include in frontend code. For more details, see [CDP API Keys](/get-started/authentication/cdp-api-keys#client-api-keys).
</Info>

## 3. Make your first request

Now let's make your first blockchain request programmatically. We'll query the current block number on Base.

<Tabs>
  <Tab title="cURL">
    ```bash theme={null}
    curl https://api.developer.coinbase.com/rpc/v1/base/YOUR_CLIENT_API_KEY \
      -H "Content-Type: application/json" \
      -d '{
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_blockNumber"
      }'
    ```

    Response:

    ```json theme={null}
    {
      "jsonrpc": "2.0",
      "id": 1,
      "result": "0x12a4b2c"
    }
    ```
  </Tab>

  <Tab title="JavaScript (fetch)">
    ```javascript theme={null}
    const rpcUrl = "https://api.developer.coinbase.com/rpc/v1/base/YOUR_CLIENT_API_KEY";

    const response = await fetch(rpcUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: 1,
        method: "eth_blockNumber",
      }),
    });

    const data = await response.json();
    console.log("Current block:", parseInt(data.result, 16));
    ```
  </Tab>

  <Tab title="Python">
    ```python theme={null}
    import requests
    import json

    rpc_url = "https://api.developer.coinbase.com/rpc/v1/base/YOUR_CLIENT_API_KEY"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_blockNumber"
    }

    response = requests.post(rpc_url, json=payload)
    result = response.json()

    # Convert hex to decimal
    block_number = int(result["result"], 16)
    print(f"Current block: {block_number}")
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript theme={null}
    const https = require("https");

    const rpcUrl = "https://api.developer.coinbase.com/rpc/v1/base/YOUR_CLIENT_API_KEY";

    const payload = JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "eth_blockNumber",
    });

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const req = https.request(rpcUrl, options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        const result = JSON.parse(data);
        console.log("Current block:", parseInt(result.result, 16));
      });
    });

    req.write(payload);
    req.end();
    ```
  </Tab>
</Tabs>

<Tip>
  **Using Ethereum libraries?** Node works with any Ethereum-compatible library like ethers.js, viem, web3.js, or web3.py. Just use your RPC endpoint URL as the provider.
</Tip>

## What to read next

* **[Core EVM Methods](/api-reference/json-rpc-api/core)**: Explore all available JSON-RPC methods
* **[Paymaster Methods](/api-reference/json-rpc-api/paymaster)**: Learn how to sponsor gas fees for your users
* **[Wallet History Methods](/api-reference/json-rpc-api/wallet-history)**: Query historical wallet data
* **[Rate Limits](/data/node/overview#rate-limits)**: Understand your usage limits and request increases
* **[CDP Discord](https://discord.com/channels/1220414409550336183/1222183017284501535)**: Join #node for support and to request rate limit increases

