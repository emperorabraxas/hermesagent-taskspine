# Use the generated HTTPS URL to test on mobile devices
```

This is particularly useful for:

* Testing embedded wallet flows on mobile browsers
* Sharing development builds with stakeholders
* Testing mobile-specific wallet connection flows

## What to test in crypto apps

### Wallet connection

Test how your app handles wallet states to prevent connection bugs and confused users.

* Disconnected → loading → connected/failed (what UI shows in each state?)
* User rejection handling (does app show clear error when user denies connection?)
* Network switching prompts (what if user is on wrong network?)

```
"Generate wallet connection tests for my [embedded/external] wallet app:

Test wallet state transitions:
- Disconnected → loading → connected/failed (UI shows each state clearly)
- User rejection handling (clear error when user denies connection)
- Network switching prompts (when user is on wrong network)

Include: React Testing Library, Jest, wallet provider mocks"
```

### Transactions

Test every step from user input to confirmation to catch gas failures and stuck transactions.

* Validate inputs and formatting
* Estimate gas (+buffers) and submit
* Track status; handle success/failure
* Surface user feedback/state updates

```
"Create transaction testing suite for my crypto app:

Test every step from user input to confirmation:
- Validate inputs and formatting
- Estimate gas (+buffers) and submit
- Track status; handle success/failure
- Surface user feedback/state updates

Focus on catching gas failures and stuck transactions.

Framework: [Jest/Vitest], mock blockchain calls"
```

### Network handling

Test multi-chain behavior and resilience when users are on wrong networks or RPCs fail.

* Detect and switch networks
* RPC failover
* Confirmations and sync across changes

```
"Generate network handling tests for multi-chain app:

Test multi-chain behavior and resilience:
- Detect and switch networks
- RPC failover
- Confirmations and sync across changes

Handle scenarios when users are on wrong networks or RPCs fail.

Mock: RPC responses, network switches, provider events"
```

## What to mock

* Wallet provider (connect, sign, send, switch, events)
* RPC calls (balances, gas, receipts)
* Contract calls (read/write)
* Transaction states (pending/success/fail)
* Network changes and errors

## Testing approaches

### Test-first approach

You can use the established Test Driven Development (TDD) methodology with AI assistance. TDD means writing tests before you write the actual code - it helps clarify what you're building and catches bugs early.

```
"Write failing tests for [feature] from requirements, then implement minimal pass, then refactor with tests green."
```

### Running tests automatically

Set up your code pipeline to run tests automatically when you make changes - this catches problems before they reach users.

```
"Generate CI config to run unit, integration, E2E on PR with cache and artifacts."
```

### Learning from bugs

When you fix a bug, write a test for it so the same problem doesn't happen again.

```
"From bug [desc], generate tests that reproduce failure, verify fix, and guard similar cases."
```

## Best practices

### Write clear test checks

Make your test assertions specific and helpful - when a test fails, you should immediately understand what went wrong.

```javascript theme={null}
// Good: Specific, meaningful assertions
expect(walletState.isConnected).toBe(true);
expect(walletState.address).toMatch(/^0x[a-fA-F0-9]{40}$/);
expect(transactionResult.hash).toBeDefined();

// Better: Custom matchers for crypto operations
expect(transaction).toBeValidTransaction();
expect(walletAddress).toBeValidEthereumAddress();
```

### Create good test data

Use realistic test data that covers common scenarios and edge cases, but keep it simple enough to understand.

```
"Generate realistic test data for crypto testing:

Data types: [wallets, transactions, tokens, prices]
Scenarios: [success cases, edge cases, errors]
Format: [TypeScript types, JSON fixtures]

Create data covering all scenarios with realistic blockchain data."
```

## What to read next

Integrate testing strategies with:

* **[AI Debugging](/get-started/develop-with-ai/development/ai-debugging)**: Use tests to prevent bugs before they happen and debug issues systematically
* **[AI Development Workflows](/get-started/develop-with-ai/development/develop-with-ai-workflows)**: Build testing into your core development process and workflow patterns
* **[AI Deployment](/get-started/develop-with-ai/development/ai-deployment)**: Ensure tests run in your deployment pipeline for reliable production releases

