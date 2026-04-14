# FAQ
Source: https://docs.cdp.coinbase.com/agent-kit/support/faq



Welcome to the Coinbase AgentKit FAQ section. Below are some of the most common questions developers have asked, along with detailed answers from our engineering team. This resource is designed to help you navigate and utilize AgentKit effectively in your projects.

### **Table of Contents**

1. [Getting Started](/agent-kit/support/faq#getting-started)
2. [Installation and Integration](/agent-kit/support/faq#installation-and-integration)
3. [Agent Architecture](/agent-kit/support/faq#agent-architecture)
4. [Network and Trading Capabilities](/agent-kit/support/faq#network-and-trading-capabilities)
5. [Wallet Management](/agent-kit/support/faq#wallet-management)
6. [Agent Functionality](/agent-kit/support/faq#agent-functionality)
7. [Support and Contributions](/agent-kit/support/faq#support-and-contributions)

## Getting Started

<AccordionGroup>
  <Accordion title="Is there a starter kit for those looking to build using AgentKit for the first time?">
    Yes. Check out our [Quickstart Guide](/agent-kit/getting-started/quickstart) and access the Replit link to get started in less than five minutes.
  </Accordion>

  <Accordion title="What's a good place to start for building agents?">
    A good starting point is to run the agent chatbot using our [repository supporting both Python and Node.js](https://github.com/coinbase/agentkit).
  </Accordion>
</AccordionGroup>

## Installation and Integration

<AccordionGroup>
  <Accordion title="What is the correct installation path for `cdp-langchain`?">
    Use the following command to install the package:

    ```
    npm install @coinbase/cdp-langchain
    ```
  </Accordion>

  <Accordion title="How can I connect the Coinbase Wallet app to my agent?">
    There are a few options available:

    1. **Seed Phrase Export:** Export the seed phrase from your Coinbase Wallet App and initialize your AgentKit agent using the seed phrase.
    2. **Fund Transfer:** Transfer funds from your Coinbase Wallet App to your agent's address.
    3. **Future Integrations:** We are actively working on deeper integrations between the Coinbase Wallet App and Agents for more seamless connectivity.
  </Accordion>
</AccordionGroup>

## Agent Architecture

<AccordionGroup>
  <Accordion title="Should I use one agent for all functions or multiple agents communicating with each other?">
    It is generally best to limit complexity where possible. Start with a single agent that supports all necessary actions. If the agent has difficulty distinguishing between actions or requires specialization for certain scenarios, you can expand your solution to include multiple agents, each focused on specific subsets of actions.
  </Accordion>
</AccordionGroup>

## Network and Trading Capabilities

<AccordionGroup>
  <Accordion title="Unfortunately, I cannot trade ETH for USDC on the Base Sepolia network, as trading features are not supported on that network. Will we be able to trade with this AI agent? What is currently developed and available, and what is planned?">
    Currently, only Base Mainnet is supported for trading feature. There are no immediate plans to support additional networks; however, we have other swap functionality features on our roadmap. Please let us know which networks you are most interested in.
  </Accordion>

  <Accordion title="Can the AI agent use other tokens to support gas fees when performing on-chain operations, such as cbBTC? It does not have USDC, ETH, or use other wallets to pay for gas.">
    USDC, EURC and cbBTC transactions are gasless for the agent on both Base Mainnet and Base Sepolia when using CDP Server Wallet. Other transactions currently require ETH for gas. You can use the faucet action to obtain Base Sepolia ETH or, if you are on Mainnet, have the agent provide its onchain address for you to send Mainnet ETH.
  </Accordion>
</AccordionGroup>

## Wallet Management

<AccordionGroup>
  <Accordion title="I'm trying to change the network the agent runs on, but it's not working. What should I do?">
    If you are using the Replit template, you may notice that there is a file called "wallet\_file.txt" that holds your agent's wallet information. If the program finds this file, it will default to giving the agent this wallet instead of creating a new one on a different network. To fix this issue, either rename the "wallet\_data.txt" file or specify a different file in the program where the wallet info will be saved.
    Note that wallet\_file.txt stores the agent's wallet seed which should be properly backed up to prevent loss of access to the wallet.
  </Accordion>

  <Accordion title="If the agent has its own wallet, is it owned by an MPC, or is there just one wallet with the signing stored locally?">
    The agent has a one-to-one wallet setup (Externally Owned Account \[EOA] with keys stored locally on the machine running the agent).
  </Accordion>

  <Accordion title="In production, how should the keys be stored? Should they be stored in the environment or in a Trusted Execution Environment (TEE)?">
    For production use cases, you can store the keys encrypted in a database, utilize a TEE, or use any other secure storage solution.
  </Accordion>

  <Accordion title="What's the limit to the number of addresses a wallet can generate?">
    Currently, the maximum number of addresses per wallet is 20 with CDP Server Wallet. Different wallet providers may have different limits, so please refer to the documentation for your specific wallet provider.
  </Accordion>

  <Accordion title="When I run the chatbot and ask it to create another address for my wallet, it says it can't. However, the Wallet documentation states that a wallet can have multiple addresses by calling `wallet.createAddress()`. Why can't the agent's wallet have multiple addresses?">
    The agent's wallet is capable of creating multiple addresses, but there is not currently an agent action to create new addresses. This functionality is on our roadmap. In the meantime, you can add a custom agent action by following our [Add Custom Functionality Guide](/agent-kit/core-concepts/agents-actions) and call `wallet.create_address(...)` within this action to enable your agent to create multiple addresses.
  </Accordion>
</AccordionGroup>

## Agent Functionality

<AccordionGroup>
  <Accordion title="How can I get real-time internet access for my agent?">
    For real-time internet access, we recommend using the [WebBrowser Tool](https://js.langchain.com/docs/integrations/tools/webbrowser/). You can add this tool to the list of tools when instantiating your agent.
  </Accordion>

  <Accordion title="What chains does AgentKit support?">
    AgentKit supports whatever networks your wallet provider supports, which will generally be most EVM-based chains. CDP Server Wallet supports the following networks:

    * Base
    * Ethereum
    * Arbitrum
    * Polygon
  </Accordion>

  <Accordion title="What wallets does AgentKit work with?">
    AgentKit works with any wallet that can connect via the [EIP-1193 standard](https://eips.ethereum.org/EIPS/eip-1193). By default, AgentKit uses CDP Server Wallet.
  </Accordion>

  <Accordion title="When referring to the `interval=10` in autonomous mode, is it 10 seconds or another unit of measurement?">
    The "interval=10" refers to 10 seconds, which is the default interval between autonomous inferences. The agent will continue to run autonomously as long as the process is active.
  </Accordion>
</AccordionGroup>

## Support and Contributions

<AccordionGroup>
  <Accordion title="I've found a bug in the AgentKit repository or have a feature request. How can I report this to the team?">
    Please open a bug report or feature request on our [AgentKit GitHub Repository](https://github.com/coinbase/agentkit/issues).
  </Accordion>
</AccordionGroup>

We hope this FAQ section helps you effectively utilize Coinbase AgentKit in your development projects.

If you have any additional questions or need further assistance, feel free to reach out through our [Coinbase Developer Platform Discord](https://discord.com/invite/cdp).

