# Start the chatbot
npm start
```

### Testing Your Agent

Try these example interactions:

```plaintext lines wrap theme={null}
You: What is your wallet address?
You: Transfer a portion of your ETH to a random address
You: What is the price of BTC?
You: Deploy an NFT that will go super viral!
You: Deploy an ERC-20 token with total supply 1 billion
```

For more detailed documentation on using Vercel AI SDK with AgentKit, see the [Vercel AI SDK integration guide](/agent-kit/core-concepts/vercel-ai-sdk).

## Model Context Protocol (MCP)

The [Anthropic Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/sdk) is a standardized protocol designed to facilitate structured interactions between AI models and external tools or APIs. This example demonstrates how to set up an MCP server integrated with AgentKit, allowing Claude Desktop to access the full set of CDP AgentKit actions.

### Prerequisites

#### Checking Node Version

Before using the example, ensure that you have Node.js 18 or higher installed. You can check your Node version by running:

```bash lines wrap theme={null}
node --version
```

If you don't have the correct version, you can install it using [nvm](https://github.com/nvm-sh/nvm):

```bash lines wrap theme={null}
nvm install node
```

#### API Keys

You'll need the following API key:

* [CDP API Key](https://portal.cdp.coinbase.com/access/api)

You'll need to configure the Claude Desktop config file with your CDP API keys. Copy the contents from `claude_desktop_config.json` to your Claude Desktop config file and update the following:

1. Update the `args` path to match the location of your built `index.js` file.
2. Set your CDP API keys in the `env` section:
   * `CDP_API_KEY_NAME`
   * `CDP_API_KEY_PRIVATE_KEY`

Then, navigate to the `claude_desktop_config.json` file found in your Claude Desktop app's settings and update its contents to match the contents of our provided `claude_desktop_config.json` file.

### Setting Up the Example

Clone the repository and navigate to the example directory:

```bash lines wrap theme={null}