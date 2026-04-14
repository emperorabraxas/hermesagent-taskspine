# AI Development Workflows
Source: https://docs.cdp.coinbase.com/get-started/develop-with-ai/development/develop-with-ai-workflows

Essential patterns for AI-first crypto development with CDP

## Overview

AI-first development treats AI as your primary development partner, not just a code completion tool. This guide covers the core workflow patterns that make crypto development faster and more effective.

**Prerequisites:** Complete [AI Development Setup](/get-started/develop-with-ai/setup/ai-development-setup) first.

## General workflow

Work in short cycles: Explore → Scaffold → Build → Refine

<Steps>
  <Step title="1. Explore">
    Start with high-level questions to understand the problem space:

    ```
    "I want to build [crypto app type]. What are the key technical decisions I need to make for CDP integration?"
    ```
  </Step>

  <Step title="2. Scaffold">
    Generate foundational code structure:

    ```
    "Create a Next.js app with CDP embedded wallets for [specific use case]. Include TypeScript types and error handling."
    ```
  </Step>

  <Step title="3. Build">
    Add features iteratively with context:

    ```
    "Add [feature] to my existing component: [paste code]. Ensure it integrates with my current patterns."
    ```
  </Step>

  <Step title="4. Refine">
    Debug, optimize, and polish:

    ```
    "Review this code for security issues: [paste code]. Focus on wallet security and transaction safety."
    ```
  </Step>
</Steps>

### Quick example

**Goal:** Add wallet connection

```
Explore: "I need wallet connection for my CDP app. What's the best approach?"
Scaffold: "Create a wallet connection component using OnchainKit with error handling"
Build: "Here's my app: [paste]. How do I integrate this component?"
Refine: "The connection works but feels slow. How can I improve the UX?"
```

## Enhanced workflow: Spec-driven development

If you're new to crypto development or using AI, you might be tempted to just start asking AI to "build me a DeFi app" and see what happens. This "vibe coding" approach can work for simple experiments, but it often leads to confusing, hard-to-debug code that doesn't actually solve your problem.

Spec-driven development gives you a structured way to turn your crypto app ideas into working code. Instead of hoping the AI guesses what you want, you guide it through a clear process your agent can follow reliably.

### Why use specs

* **Prevents overwhelming complexity:** Without a spec, AI might build a complex DeFi protocol when you just wanted a simple token swap
* **Teaches you crypto concepts:** Writing specs forces you to understand wallets, networks, and transactions before coding
* **Creates maintainable code:** Structured planning leads to code you can actually understand and modify later
* **Reduces debugging time:** Clear requirements mean fewer "why doesn't this work?" moments

### Process and tools

Follow these four steps to transform vague crypto ideas into working applications:

<Steps>
  <Step title="1. Write your app specification">
    Start by clearly describing what you want to build and why. You don't need to go too far into the details, but you should provide a good understanding of the app you want to build:

    ```
    "Write a detailed specification for a simple crypto tip jar app:

    Purpose: Let content creators receive crypto tips from fans
    Target users: Streamers and bloggers who are new to crypto
    Core features:
    - Generate a unique tip page with QR code
    - Accept USDC tips on Base network  
    - Show tip history and total earnings
    - Send email notifications for new tips

    User experience:
    - Creator signs up with email (no crypto knowledge needed)
    - Embedded wallet handles all crypto complexity
    - Fans can tip with credit card or existing wallet
    - Creator can withdraw to bank account or keep in crypto

    Success criteria:
    - Creator can set up tip page in under 2 minutes
    - Fans can send tips without owning crypto
    - 99% uptime for tip processing"
    ```

    **Helpful tools for this step:**

    * **[Claude](https://claude.ai/)** - Excellent at creating detailed, well-structured specifications
    * **[GitBook](https://gitbook.com/)** - If you want collaborative spec writing with your team
  </Step>

  <Step title="2. Get a technical architecture plan">
    Ask AI to design the technical structure based on your spec:

    ```
    "Based on this tip jar specification, create a detailed technical architecture plan.

    Consider these requirements:
    - Must use CDP embedded wallets for easy onboarding
    - Should work on Base network for low fees
    - Needs to handle both crypto and credit card payments
    - Must be beginner-friendly for creators

    Please include:
    - Recommended frontend framework and why
    - Database design for users and transactions
    - Payment processing architecture
    - Component breakdown with responsibilities
    - Security considerations and best practices
    - Integration points with CDP services

    Focus on a simple, maintainable architecture that a beginner developer can understand and implement."
    ```

    **Helpful tools for this step:**

    * **[ChatGPT](https://chat.openai.com/)** - Great at architectural planning and explaining technical decisions
    * **[Cursor](https://cursor.sh/)** - AI-first editor that can help refine architecture with CDP context
    * **[CDP MCP Server](https://docs.cdp.coinbase.com/mcp)** - Gives AI direct access to CDP documentation for accurate architecture suggestions
  </Step>

  <Step title="3. Get a development task list">
    Ask AI to break the architecture into specific, manageable tasks:

    ```
    "Based on this tip jar architecture, create a prioritized development task list for a beginner developer.

    Break it into 3 phases over 3 weeks, with 4 tasks per phase. Each task should take 2-4 hours to complete.

    For each task, include:
    - Clear task description and goal
    - Specific code files to create or modify
    - Testing steps to verify it works
    - Common issues beginners might face
    - Dependencies on other tasks

    Start with basic setup, then core functionality, then user experience improvements."
    ```

    **Helpful tools for this step:**

    * **[Spec Kit](https://github.com/github/spec-kit)** - Specifically designed to break specs into actionable tasks
    * **[Linear](https://linear.app/)** - Perfect for organizing and tracking AI-generated task breakdowns
    * **[Height](https://height.app/)** - Automatically organizes tasks with dependencies and estimates
  </Step>

  <Step title="4. Implement with guided prompts">
    Use the task list to create focused implementation requests:

    ```
    "Implement Task 1.2: Configure CDP SDK and embedded wallets

    Project context: Crypto tip jar app for content creators
    Current progress: Next.js project is set up
    This task goal: Enable creators to connect wallets easily

    Requirements from spec:
    - Embedded wallets for users new to crypto
    - Base network for low transaction fees
    - Simple connection flow (no complex wallet setup)

    Technical constraints from architecture:
    - Use CDP Web SDK
    - Store wallet addresses in our database
    - Handle connection errors gracefully

    Expected outcome:
    - Creator can connect wallet in 2 clicks
    - App stores wallet address for future tips
    - Clear error messages if connection fails

    Please provide:
    1. Complete code for wallet connection component
    2. Error handling for common connection issues
    3. Instructions for testing the connection flow"
    ```

    **Helpful tools for this step:**

    * **[Cursor](https://cursor.sh/)** - AI-first editor perfect for implementing with full project context
    * **[GitHub Copilot](https://github.com/features/copilot)** - Excellent code completion for implementing specific tasks
    * **[Replit](https://replit.com/)** - Cloud environment great for quick prototyping and testing
    * **[ngrok](https://ngrok.com/)** - Create secure tunnels to test your crypto app on mobile devices and share with others
  </Step>
</Steps>

## When to use each approach

Now that you understand both the general workflow and spec-driven development, here's how to choose the right approach for your situation:

**Use spec-driven development for:**

* **Your first crypto application** - The structure helps you learn concepts properly
* **Apps handling real money or user funds** - Detailed planning prevents costly security mistakes
* **Multi-feature applications** - Specs keep complex projects organized and maintainable
* **Team projects** - Clear specifications help everyone understand the system
* **Learning projects** - Forces you to understand each component before building it

**Use the lighter general workflow for:**

* **Quick experiments** with new CDP features or proof-of-concepts
* **Simple UI changes** or styling updates to existing apps
* **Bug fixes** where the problem and solution are already clear
* **Prototyping ideas** before committing to full specifications

## Structured vs. freeform

There's a spectrum between highly structured specification-driven development and more flexible, exploratory coding approaches. For crypto development, structured specs provide important benefits:

**Vibe coding issues:**

* AI assumes you understand crypto concepts you might not know yet
* Code becomes hard to debug when transactions fail
* Security issues from incomplete understanding of wallet interactions
* Feature creep leads to overwhelming complexity

**Spec-driven benefits for beginners:**

* Forces you to learn crypto concepts before implementing them
* Creates code you can understand and modify
* Prevents common security mistakes through structured planning
* Builds confidence through clear, achievable milestones

## Best practices

### Always validate AI code

```
"Review this code for:
- Security vulnerabilities
- Performance issues
- Integration problems"
```

### Build incrementally

Start simple, add complexity gradually. Don't try to build everything at once.

### Maintain context

Reference previous conversations: "Based on our discussion about \[feature], now help me add \[next part]"

## Example workflows

* **Adding a new feature:** Explore → Design → Implement → Integrate → Test
* **Fixing a bug:** Isolate → Analyze → Fix → Prevent
* **Optimizing performance:** Analyze → Identify bottlenecks → Optimize → Validate

## What to read next

Start with the specialized technique most relevant to your current need:

* **[AI Prompting Techniques](/get-started/develop-with-ai/development/ai-prompting-techniques)**: Master effective prompting patterns for better AI responses
* **[Debugging AI Code](/get-started/develop-with-ai/development/ai-debugging)**: Systematic approaches to fix issues when code doesn't work as expected
* **[Testing Strategies](/get-started/develop-with-ai/development/ai-testing)**: Comprehensive testing approaches for AI-generated crypto applications
* **[AI Deployment](/get-started/develop-with-ai/development/ai-deployment)**: Deploy your crypto application with AI assistance

