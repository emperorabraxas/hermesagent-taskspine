# AI-Assisted Testing Strategies
Source: https://docs.cdp.coinbase.com/get-started/develop-with-ai/development/ai-testing

Essential approaches to testing AI-generated crypto applications with automated test generation

## Overview

When you're building crypto apps with AI assistance, testing is very important (especially around wallets, transactions, and network connections). The good news is you can use AI to help write tests quickly, then improve them as needed.

## Types of tests

### Unit tests

These tests check individual pieces of code in isolation, like testing a single function or component.

```
"Generate unit tests for:
Code: [paste]
Framework: [Jest/Vitest + RTL]
Cover: interactions, error states, loading.
Mock: wallet/RPC as needed."
```

### Integration tests

Integration tests check how different parts of your app work together - like how your wallet component talks to your transaction component.

```
"Create integration tests for flow:
App: [embedded wallet/DeFi]
Steps: [list]
Cover: happy path, wallet disconnect, tx failure, state sync."
```

### End-to-end tests

End-to-end tests check complete user flows in a real browser or mobile app - like a user connecting their wallet, sending money, and seeing the confirmation.

```
"Design E2E tests:
Journeys: [onboarding, send, swap]
Tool: [Playwright/Cypress]
Include: error handling, mobile, cross-browser, wallet mock."
```

### Mobile testing

When building embedded wallet or mobile-first crypto apps, testing on actual devices is crucial for catching touch interactions, mobile wallet connections, and performance issues.

**[ngrok](https://ngrok.com/docs) for mobile testing:**

* Creates secure HTTPS tunnels to your local development server
* Allows testing your local app on real mobile devices
* Essential for testing mobile wallet integrations and embedded wallet flows

```bash theme={null}