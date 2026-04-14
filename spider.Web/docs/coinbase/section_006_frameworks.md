# Frameworks
Source: https://docs.cdp.coinbase.com/agent-kit/core-concepts/frameworks



AgentKit integrates with several popular AI frameworks, enabling you to build blockchain-capable agents using your preferred development tools.

<Tip>
  Visit our [Quickstart Guide](/agent-kit/getting-started/quickstart) to bootstrap your project.
</Tip>

The following frameworks are currently supported:

* [Agents SDK by OpenAI](#agents-sdk-by-openai)
* [LangChain](#langchain)
* [Eliza](#eliza-framework)
* [Vercel AI SDK](#vercel-ai-sdk)
* [Model Context Protocol (MCP)](#model-context-protocol-mcp)

## Agents SDK by OpenAI

The [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents) is a lightweight, Python-first framework that enables you to build production-ready AI agents with minimal abstractions. It's designed to be easy to learn while providing powerful capabilities for real-world applications.

You can find our implementation in our [Replit template](https://replit.com/t/coinbase-developer-platform/repls/CDP-AgentKit-Agents-SDK-Quickstart/view#README.md) or the [AgentKit repository](https://github.com/coinbase/agentkit/).

<Tabs>
  <Tab title="Replit">
    #### Step 1: Set Up Your Development Environment

    1. Fork the [Python](https://replit.com/t/coinbase-developer-platform/repls/CDP-AgentKit-Agents-SDK-Quickstart/view#README.md) template
    2. Once forked, you'll have your own version of the project to modify

    #### Step 2: Configure Environment Variables

    1. Click on "Tools" in the left sidebar
    2. Select "Secrets"
    3. Add the following secrets:

    ```bash lines wrap theme={null}
    CDP_API_KEY_NAME=your_cdp_key_name # From cdp.coinbase.com
    CDP_API_KEY_PRIVATE_KEY=your_cdp_private_key
    OPENAI_API_KEY=your_openai_key # from platform.openai.com
    NETWORK_ID="base-sepolia" # Optional, defaults to base-sepolia.
    ```

    #### Step 3: Run the Agent

    You can start this chatbot by clicking the "Run" button.

    <Warning>
      Security of wallets on Replit template

      Every agent comes with an associated wallet. Wallet data is read from wallet\_data.txt, and if that file does not exist, this repl will create a new wallet and persist it in a new file. Please note that this contains your wallet's private key and should not be used in production environments. Refer to the [CDP Server Wallet](/server-wallets/v2/introduction/welcome) on how to secure your wallets.
    </Warning>
  </Tab>

  <Tab title="Local Environment (repository)">
    #### Step 1: Clone the repository

    Ensure that you have Python 3.10+ and Poetry installed:

    ```bash lines wrap theme={null}
    python --version  # Should be 3.10+
    poetry --version  # Make sure Poetry is installed
    ```

    Clone and navigate to the example directory:

    ```bash lines wrap theme={null}
    # Clone the repository
    git clone https://github.com/coinbase/agentkit.git

    # Navigate to the chatbot-python example
    cd agentkit/python/examples/openai-agents-sdk-cdp-chatbot
    ```

    #### Step 2: Configure Environment Variables

    Copy the example environment file and configure your variables:

    ```bash lines wrap theme={null}
    # Copy the example environment file
    cp .env.local .env

    # Edit the .env file with your credentials:
    CDP_API_KEY_NAME=your_cdp_key_name # From cdp.coinbase.com
    CDP_API_KEY_PRIVATE_KEY=your_cdp_private_key
    OPENAI_API_KEY=your_openai_key # from platform.openai.com
    NETWORK_ID="base-sepolia" # Optional, defaults to base-sepolia.
    ```

    #### Step 3: Run the Agent

    ```bash lines wrap theme={null}
    # Install dependencies
    poetry install

    # Run the chatbot
    poetry run python chatbot.py
    ```
  </Tab>
</Tabs>

## LangChain

[LangChain](https://www.langchain.com/) is a framework for developing applications powered by language models. Our implementation is available in our [Replit templates](https://replit.com/t/coinbase-developer-platform/profile) and the [AgentKit repository](https://github.com/coinbase/agentkit/).

<Tabs>
  <Tab title="Replit">
    #### Step 1: Set Up Your Development Environment

    1. Fork the template from [NodeJS (EVM)](https://replit.com/t/coinbase-developer-platform/repls/AgentKitjs-Quickstart-020-EVM-CDP-Wallet/view), [Python (EVM)](https://replit.com/t/coinbase-developer-platform/repls/AgentKitpy-012-EVM/view), or [NodeJS (Solana)](https://replit.com/t/coinbase-developer-platform/repls/AgentKitjs-Solana-Quickstart-v020/view) Replit templates
    2. Once forked, you'll have your own version of the project to modify

    #### Step 2: Configure Environment Variables

    1. Click on "Tools" in the left sidebar
    2. Select "Secrets"
    3. Add the following secrets:

    <CodeGroup>
      ```plaintext EVM lines wrap theme={null}
      CDP_API_KEY_NAME=your_cdp_key_name
      CDP_API_KEY_PRIVATE_KEY=your_cdp_private_key
      OPENAI_API_KEY=your_openai_key
      NETWORK_ID="base-sepolia" # Optional, defaults to base-sepolia.
      MNEMONIC_PHRASE=your_mnemonic_phrase # Optional, if it is not provided the agent will create a new wallet
      ```

      ```plaintext Solana lines wrap theme={null}
      OPENAI_API_KEY=your_openai_key
      SOLANA_PRIVATE_KEY=your_solana_private_key # Optional, if it is not provided the agent will create a new wallet
      NETWORK_ID="solana-devnet" # Optional, defaults to solana-devnet. Can also be "solana-mainnet", "solana-testnet"
      ```
    </CodeGroup>

    #### Step 3: Run the Agent

    You can start this chatbot by clicking the "Run" button.

    <Tabs>
      <Tab title="EVM">
        <Warning>
          Security of wallets on Replit template

          Every agent comes with an associated wallet. Wallet data is read from `wallet_data.txt`; if that file does not exist, this Repl will create a new wallet and save it to a new file. Please note that this file contains your wallet's private key and should not be used in production environments. Refer to the [CDP Server Wallets](/server-wallets/v2/introduction/welcome) on securing wallets for production use.
        </Warning>
      </Tab>

      <Tab title="Solana">
        For Solana, note that the private key is not stored in a file but rather in the environment variable `SOLANA_PRIVATE_KEY`. For Replit to work with an address, you must add the secret `SOLANA_PRIVATE_KEY` with your private key as the value.

        If you're using the devnet or testnet, you can get test SOL from the [Solana Faucet](https://faucet.solana.com/).
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Local Environment">
    #### Step 1: Set Up Your Development Environment

    <Tabs>
      <Tab title="Typescript">
        Ensure that you have Node.js 18+ installed:

        ```bash lines wrap theme={null}
        node --version  # Should be 18+
        npm --version   # Should be 9.7.2+
        ```

        Clone and set up the repository:

        ```bash lines wrap theme={null}
        # Clone the repository
        git clone https://github.com/coinbase/agentkit.git

        # Navigate to the root of the typescript monorepo
        cd agentkit/typescript

        # Install dependencies
        npm install

        # Build the packages locally
        npm run build

        # Navigate to the langchain-cdp-chatbot example or the langchain-solana-chatbot
        cd examples/langchain-cdp-chatbot
        ```
      </Tab>

      <Tab title="Python">
        Ensure that you have Python 3.10+ and Poetry installed:

        ```bash lines wrap theme={null}
        python --version  # Should be 3.10+
        poetry --version  # Make sure Poetry is installed
        ```

        Clone and navigate to the example directory:

        ```bash lines wrap theme={null}
        # Clone the repository
        git clone https://github.com/coinbase/agentkit.git

        # Navigate to the chatbot-python example
        cd agentkit/python/examples/langchain-cdp-chatbot
        ```
      </Tab>
    </Tabs>

    #### Step 2: Configure Environment Variables

    <Tabs>
      <Tab title="Typescript">
        Copy the example environment file and configure your variables:

        <CodeGroup>
          ```bash EVM lines wrap theme={null}
          # Copy the example environment file
          cp .env.local .env

          # Edit the .env file with your credentials:
          # CDP_API_KEY_NAME=your_cdp_key_name
          # CDP_API_KEY_PRIVATE_KEY=your_cdp_private_key
          # OPENAI_API_KEY=your_openai_key
          # NETWORK_ID=base-sepolia  # Optional, defaults to base-sepolia
          ```

          ```bash Solana lines wrap theme={null}
          # Copy the example environment file
          cp .env.local .env

          # OPENAI_API_KEY=your_openai_key
          # SOLANA_PRIVATE_KEY=your_solana_private_key # Optional, if it is not provided the agent will create a new wallet
          # NETWORK_ID="solana-devnet" # Optional, defaults to solana-devnet. Can also be "solana-mainnet", "solana-testnet"
          ```
        </CodeGroup>
      </Tab>

      <Tab title="Python">
        Copy the example environment file and configure your variables:

        ```bash lines wrap theme={null}
        # Copy the example environment file
        cp .env.example .env

        # Edit the .env file with your credentials:
        # CDP_API_KEY_NAME=your_cdp_key_name
        # CDP_API_KEY_PRIVATE_KEY=your_cdp_private_key
        # OPENAI_API_KEY=your_openai_key
        # NETWORK_ID=base-sepolia  # Optional, defaults to base-sepolia. On Solana, this can be "solana-mainnet", "solana-devnet" (default), or "solana-testnet"
        ```
      </Tab>
    </Tabs>

    #### Step 3: Run the Agent

    <Tabs>
      <Tab title="Typescript">
        ```bash lines wrap theme={null}
        # Run the chatbot
        npm run start
        ```
      </Tab>

      <Tab title="Python">
        ```bash lines wrap theme={null}
        # Install dependencies
        poetry install

        # Run the chatbot
        make run
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

**Common Issues**

* If you're trying to switch networks and your agent will not change, try renaming the `wallet_data.txt` file. Each network requires a new wallet, and if the program identifies a previously-created wallet it will not create the new one on the new network.

### Adding Agent Functionality

Extend your agent with chat capabilities. To add more functionality, see the [agent actions](/agent-kit/core-concepts/agents-actions) guide.

### Testing Your Agent

Try these example interactions:

```bash lines wrap theme={null}
You: What is your wallet address?
You: transfer .001 ETH to 0x4c8bbcfc6DaE447228FcbB220C1DD4cae623EaaF
You: Register a basename for yourself that represents your identity
```

## Eliza Framework

[Eliza](https://github.com/elizaOS/eliza) is a framework for building AI agents with a focus on simplicity and extensibility. For a detailed walkthrough, see our [video tutorial](https://www.youtube.com/live/DlRR1focAiw).

<Warning>
  Compatibility Note

  When creating your CDP API key in the portal, make sure to select `ECDSA` as the signature algorithm. The Eliza framework integration requires CDP API keys configured with the `ECDSA` signature algorithm. `Ed25519` signatures are not currently supported.
</Warning>

```bash lines wrap theme={null}
npx create-agentkit-app my-agent
cd my-agent
cp .env.example .env