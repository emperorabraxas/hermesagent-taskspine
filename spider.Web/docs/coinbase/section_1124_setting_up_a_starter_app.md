# Setting up a starter app
Source: https://docs.cdp.coinbase.com/get-started/develop-with-ai/setup/ai-development-setup

Configure your development environment for optimal AI-assisted crypto development with CDP

This guide walks you through the process of setting up a sample app with source code to help you get started with AI-assisted crypto development with Coinbase Developer Platform (CDP).

## Prerequisites

* [Coinbase Developer Platform account](https://portal.cdp.coinbase.com/) for access to our APIs
* AI development environment: [Cursor IDE](https://cursor.sh/) (recommended), [GitHub Copilot](https://github.com/features/copilot), [Claude](https://claude.ai/), or [ChatGPT](https://chat.openai.com/)
* `npm` for setting up starter apps

## 1. Choose a starter app

Start with the right starter app depending on your needs.

Use this quick mapping:

* If you want seamless onboarding with embedded wallets for consumers → choose **Consumer-based apps**.
* If you need external wallet connections and DeFi protocol integrations → choose **Trading apps (DeFi)**.
* If your core is automation, bots, or 24/7 server-side operations → choose **Automation and AI Agents**.

### Comparison

| App type                 | Best for                                                                                                                   | Why it works with AI                                                                                                                          | Starter prompt                                                                                                            |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Consumer-based apps      | <ul><li>Payment apps</li><li>Social crypto features</li><li>Consumer wallets</li><li>Tipping systems</li></ul>             | <ul><li>Embedded-wallet patterns</li><li>Common flows</li><li>Simpler security</li><li>Rapid UI iteration</li></ul>                           | I'm building a consumer app with embedded wallets. Help me add \[feature] that works with email auth and no seed phrases. |
| Trading apps (DeFi)      | <ul><li>DEX interfaces</li><li>Portfolio trackers</li><li>Yield farming apps</li><li>Advanced trading tools</li></ul>      | <ul><li>OnchainKit patterns</li><li>External wallet integration</li><li>Rich DeFi ecosystem</li><li>AI helps with complex state</li></ul>     | I'm building a DeFi app with OnchainKit and wagmi. Help me create \[feature] integrating with \[protocol].                |
| Automation and AI Agents | <ul><li>Trading bots</li><li>Automated portfolio management</li><li>Cross-chain operations</li><li>Data analysis</li></ul> | <ul><li>AgentKit AI-native patterns</li><li>Built-in CDP SDK</li><li>AI-assisted automation design</li><li>Server-side for 24/7 ops</li></ul> | I'm building an AI agent with AgentKit and CDP SDK. Help me automate \[goal] with robust error handling and monitoring.   |

## 2. Scaffold your project

<Tabs>
  <Tab title="Consumer App">
    ```bash theme={null}
    npm create @coinbase/cdp-app@latest my-consumer-app
    ```

    You will be prompted to choose a template type and configure your project. This starter app works with the CDP Web SDK for embedded wallets, email authentication, and no seed phrases required.

    Find more detailed instructions on its setup in the [Embedded Wallet Guide](/embedded-wallets/quickstart).
  </Tab>

  <Tab title="DeFi App">
    ```bash theme={null}
    npm create onchain@latest my-defi-app
    ```

    You will be prompted to choose a template type and configure your project. This starter app works with OnchainKit for external wallet connections, DeFi protocol integrations, and advanced trading features.

    Find more detailed instructions on its setup in the [OnchainKit Getting Started Guide](https://onchainkit.xyz/getting-started).
  </Tab>

  <Tab title="AI Agent">
    ```bash theme={null}
    npm create onchain-agent@latest my-agent
    ```

    You will be prompted to choose a template type and configure your project. This starter app works with AgentKit for building AI agents that can interact with blockchain networks, including trading, automated portfolio management, and 24/7 server-side operations.

    Find more detailed instructions on its setup in the [AgentKit Quickstart Guide](/agent-kit/getting-started/quickstart).
  </Tab>
</Tabs>

### Integrating starter apps

For complex projects that need features from multiple templates, you can start with one and use AI to integrate patterns from others:

**Consumer + DeFi Integration:**

```bash theme={null}