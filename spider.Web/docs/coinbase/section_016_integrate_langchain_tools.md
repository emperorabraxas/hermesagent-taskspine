# Integrate LangChain Tools
Source: https://docs.cdp.coinbase.com/agent-kit/core-concepts/integrate-langchain-tools



LangChain has revolutionized the way developers interact with language models and build powerful AI applications. One of its most compelling features is the extensive ecosystem of tools and integrations that allow developers to quickly and easily extend their agents' capabilities.

## The Power of LangChain Tools

LangChain's true strength lies in its [vast array of community-supported tools and integrations](https://python.langchain.com/docs/integrations/tools/). These tools enable developers to:

* **Rapidly expand agent capabilities**: Integrate with various APIs, databases, and services without writing extensive custom code
* **Leverage specialized functionalities**: Access domain-specific tools for tasks like image generation, social media posting and consumption, internet search, data analysis, or blockchain interactions
* **Create multi-modal agents**: Combine different types of interactions (text, image, code) within a single agent
* **Stay up-to-date**: Benefit from a constantly growing ecosystem of tools maintained by the community

By utilizing these tools, developers can create sophisticated AI agents that can perform a wide range of tasks, from generating images to sending emails, all through natural language interfaces.

## Adding the Dall-E Image Generator to Your Agent

In this guide, we'll walk through the process of adding the Dall-E Image Generator tool to an existing LangChain agent. This will demonstrate how easily you can enhance your agent's capabilities using community toolkits.

### Prerequisites

* An existing AgentKit setup, like the one in our [Replit template](https://replit.com/@CoinbaseDev/CDP-AgentKit#README.md)
* Python 3.10+ or NodeJS 18+
* OpenAI API key

### Step 1: Install Required Packages

First, ensure you have the necessary packages installed:

<CodeGroup>
  ```bash Typescript lines wrap theme={null}
  npm install @langchain/openai
  ```

  ```bash Python lines wrap theme={null}
  pip install langchain-community
  ```
</CodeGroup>

### Step 2: Import Required Modules

Add the following imports to your existing imports:

<CodeGroup>
  ```typescript Typescript lines wrap theme={null}
  import { DallEAPIWrapper } from "@langchain/openai";
  ```

  ```python Python lines wrap theme={null}
  from langchain.agents import load_tools
  from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
  ```
</CodeGroup>

### Step 3: Set Up OpenAI API Key

If you haven't already, set up your OpenAI API key as an environment variable and ensure the account is funded:

<CodeGroup>
  ```bash Typescript lines wrap theme={null}
  export OPENAI_API_KEY="your_api_key"
  ```

  ```bash Python lines wrap theme={null}
  export OPENAI_API_KEY="your_api_key"
  ```
</CodeGroup>

### Step 4: Load the Dall-E Tool

Before initializing your agent, load the Dall-E tool:

<CodeGroup>
  ```typescript Typescript lines wrap theme={null}
  const dallETool = new DallEAPIWrapper({
    n: 1,
    model: "dall-e-3",
    apiKey: process.env.OPENAI_API_KEY,
  });
  ```

  ```python Python lines wrap theme={null}
  dalle_tool = load_tools(["dalle-image-generator"])
  ```
</CodeGroup>

### Step 5: Combine Tools

Add the Dall-E tool to your existing tools:

<CodeGroup>
  ```typescript Typescript lines wrap theme={null}
  const allTools = [...getLangChainTools(agentkit), dallETool];
  ```

  ```python Python lines wrap theme={null}
  all_tools = get_langchain_tools(agentkit) + dalle_tool
  ```
</CodeGroup>

### Step 6: Update Agent Initialization

Modify your create\_react\_agent call to include the new tools:

<CodeGroup>
  ```typescript Typescript lines wrap theme={null}
  async function initializeAgent() {
    // Initialize LLM
    const llm = new ChatOpenAI({
      model: "gpt-4o-mini",
    });

    // ... (previously mentioned code for creating and instantiating tools) ...

    // Create React Agent using the LLM and CDP AgentKit tools
    const agent = createReactAgent({
      llm,
      tools: allTools,
      checkpointSaver: memory,
      messageModifier:
      "You are a helpful agent that can interact onchain using the Coinbase Developer Platform AgentKit...",
    });

    return { agent, config: agentConfig };
  }
  ```

  ```python Python lines wrap theme={null}
  def initialize_agent():
    """Initialize the agent with CDP AgentKit and Dall-E."""
    llm = ChatOpenAI(model="gpt-4o-mini")

    # ... (previously mentioned code for creating and instantiating tools) ...

    return create_react_agent(
      llm,
      tools=all_tools,
      checkpointer=memory,
      state_modifier="You are a helpful agent that can interact onchain using the Coinbase Developer Platform AgentKit...",
    ), config
  ```
</CodeGroup>

Now your agent is equipped with the ability to generate images using Dall-E alongside its existing CDP capabilities. You can test it by asking the agent to generate images through natural language requests.

For more information on available tools and integration options, visit the [LangChain documentation](https://python.langchain.com/docs/how_to/#tools).

