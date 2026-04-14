# Navigate to the MCP client example
cd clients/mcp
```

### 2. Configure Claude Desktop

Add the MCP server to your Claude Desktop configuration:

```json theme={null}
{
  "mcpServers": {
    "demo": {
      "command": "pnpm",
      "args": [
        "--silent",
        "-C",
        "<absolute path to this repo>/examples/typescript/clients/mcp",
        "dev"
      ],
      "env": {
        "EVM_PRIVATE_KEY": "<private key of a wallet with USDC on Base Sepolia>",
        "SVM_PRIVATE_KEY": "<base58-encoded private key of a Solana wallet with USDC on Devnet>",
        "RESOURCE_SERVER_URL": "http://localhost:4021",
        "ENDPOINT_PATH": "/weather"
      }
    }
  }
}
```

### 3. Start the x402 Server

Make sure your x402-compatible server is running at the URL specified in `RESOURCE_SERVER_URL`:

```bash theme={null}