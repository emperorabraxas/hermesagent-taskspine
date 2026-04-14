# Core JSON-RPC Methods
Source: https://docs.cdp.coinbase.com/api-reference/json-rpc-api/core

The following EVM-compatible JSON-RPC methods provide convenient access to onchain data on Base.

## Constructing Requests

**Option 1**: You can use the [JSON-RPC playground](https://portal.cdp.coinbase.com/products/node) to easily create sample JSON-RPC requests.

**Option 2**: Alternatively, you can construct your own requests by following the below steps:

1. Go to the [Node](https://portal.cdp.coinbase.com/products/node) page in the CDP Portal.
2. Ensure the correct network in your RPC URL (either `base` or `base-sepolia`).
3. Open a terminal and make your requests based on the supported methods in this API reference page.

<Info>
  **Authentication**

  For information on how to authenticate requests to our JSON-RPC APIs, please visit the **Client API Keys** section of our [Authentication page](/get-started/authentication/cdp-api-keys#client-api-keys).
</Info>

## Batch Requests

Below is an example of a [batch request](https://www.jsonrpc.org/specification#batch) for a JSON-RPC API method.

> Batch request example of `eth_getTransactionReceipt`

```bash lines wrap theme={null}
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '[{"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionReceipt", "params": ["0x633982a26e0cfba940613c52b31c664fe977e05171e35f62da2426596007e249"]}, { "jsonrpc": "2.0", "id": 2, "method": "eth_getTransactionReceipt", "params": ["0x3a7d521b20b5684e0e9ec14aeebe8ccab67137f7d5c2589efb55b0625fcc9c6d"]}]'
```

## Ethereum Namespace

Below are example requests for JSON-RPC API methods in the `eth_*` namespace.

<Info>
  For API methods in the `eth_*` namespace, we only support the following block tags: `latest`, `earliest`, and block number in hex format.
</Info>

### `eth_blockNumber`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}