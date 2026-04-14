# Navigate to the MCP example directory
cd typescript/examples/model-context-protocol-cdp-server
```

Configure your Claude Desktop by updating the `claude_desktop_config.json` file with your CDP API keys and the correct path to your built `index.js` file.

To use the chatbot, simply open Claude Desktop after configuring your API keys. The MCP server will run automatically when you interact with Claude.

### Testing Your Agent

Try these example interactions in Claude Desktop:

```plaintext lines wrap theme={null}
Transfer a portion of your ETH to a random address
What is the price of BTC?
Deploy an NFT that will go super viral!
Deploy an ERC-20 token with total supply 1 billion
```

For more detailed documentation on using MCP with AgentKit, see the [Model Context Protocol extension information](/agent-kit/core-concepts/model-context-protocol).

