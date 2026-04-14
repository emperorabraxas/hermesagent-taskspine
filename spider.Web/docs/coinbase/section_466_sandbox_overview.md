# Sandbox Overview
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/sandbox/overview

Test your payment integrations in a safe, isolated environment

<Info>
  Sandbox uses the same API endpoints, authentication, and response formats as production. Behavior is simulated (no real transactions), making it easy to transition your code when ready.
</Info>

## Key concepts in Sandbox

| Resource                                                                                                        | Direction       | Description                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **[Account](/api-reference/payment-apis/rest-api/accounts/accounts)**                                           | -               | Your asset balance within Coinbase that you fund with test amounts (e.g., your USD balance with \$1000 test funds)                                                       |
| **[Deposit destination](/api-reference/payment-apis/rest-api/deposit-destinations-under-development/overview)** | Incoming crypto | Placeholder addresses for receiving crypto. Simulate deposits via Portal UI                                                                                              |
| **[Payment method](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)**                      | Outgoing fiat   | External bank accounts for fiat withdrawals. Three pre-configured test banks shared across all accounts (Fedwire JPMorgan, Fedwire Bank of America, SWIFT Deutsche Bank) |
| **[Transfer](/api-reference/payment-apis/rest-api/transfers/transfers)**                                        | Both            | Move funds to crypto addresses, emails, or payment methods. All simulated                                                                                                |

## Sandbox vs. Production

Sandbox and production offer the same endpoints and functionality, but with different data and behavior.

### Operational differences

|                          | Sandbox                      | Production                      |
| ------------------------ | ---------------------------- | ------------------------------- |
| **Base URL**             | `sandbox.cdp.coinbase.com`   | `api.cdp.coinbase.com`          |
| **API keys**             | Sandbox-specific credentials | Production credentials          |
| **Rate limits**          | Same as production           | Standard production limits      |
| **Data persistence**     | Permanent                    | Permanent                       |
| **Performance**          | Response times may vary      | Standard production performance |
| **Third-party services** | Mocked responses             | Real integrations               |
| **Compliance checks**    | Simplified (no real KYC/AML) | Full compliance flows           |

### Resource differences

|                                                                                                                  | Sandbox                                                                  | Production                                                 |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------- |
| **[Accounts](/api-reference/payment-apis/rest-api/accounts/accounts)**                                           | Create via Sandbox UI (funding only via UI)                              | Link existing Prime portfolio or Coinbase Business account |
| **[Deposit destinations](/api-reference/payment-apis/rest-api/deposit-destinations-under-development/overview)** | Placeholder addresses; simulate deposits via Sandbox UI                  | Real blockchain addresses                                  |
| **[Payment methods](/api-reference/payment-apis/rest-api/payment-methods/payment-methods)**                      | Three test methods: Fedwire (active), Fedwire (inactive), SWIFT (active) | Automatically linked from Prime/Business                   |
| **[Transfers](/api-reference/payment-apis/rest-api/transfers/transfers)**                                        | Simulated (webhooks fire, no blockchain activity)                        | Real blockchain transactions                               |
| **[Webhooks](/api-reference/payment-apis/webhooks)**                                                             | Supported                                                                | Supported                                                  |

<Info>
  **Fully simulated - no blockchain connectivity.** All transactions are simulated within Sandbox—no mainnet or testnet. This allows faster, more reliable testing.
</Info>

## Best practices

<AccordionGroup>
  <Accordion title="Isolate Sandbox configuration">
    Keep Sandbox configuration completely separate from production:

    ```typescript theme={null}
    // config.ts
    const config = {
      sandbox: {
        apiUrl: 'https://sandbox.cdp.coinbase.com',
        apiKey: process.env.CDP_SANDBOX_API_KEY,
      },
      production: {
        apiUrl: 'https://api.cdp.coinbase.com',
        apiKey: process.env.CDP_PRODUCTION_API_KEY,
      }
    };

    export const getConfig = () => {
      return process.env.NODE_ENV === 'production'
        ? config.production
        : config.sandbox;
    };
    ```
  </Accordion>

  <Accordion title="Test error handling">
    Use Sandbox to thoroughly test error scenarios:

    * Invalid authentication
    * Malformed requests
    * Rate limiting
    * Network timeouts
    * Insufficient funds
    * Invalid account details
  </Accordion>

  <Accordion title="Automate integration tests">
    Create automated test suites that run against Sandbox:

    ```typescript theme={null}
    // tests/integration/payments.test.ts
    describe('Payments API Integration', () => {
      beforeAll(() => {
        // Set up sandbox client
      });

      test('should process transfer', async () => {
        const transfer = await createTransfer({
          amount: '100.00',
          currency: 'USD'
        });

        expect(transfer.status).toBe('pending');
      });
    });
    ```
  </Accordion>

  <Accordion title="Monitor API usage">
    Track your API usage patterns in Sandbox to understand production requirements:

    * Request volumes
    * Response times
    * Error rates
    * Rate limit consumption
  </Accordion>
</AccordionGroup>

## What to read next

<CardGroup>
  <Card title="Quickstart" icon="rocket" href="/api-reference/payment-apis/sandbox/quickstart">
    Set up your API keys and make your first Sandbox request
  </Card>

  <Card title="Troubleshooting" icon="wrench" href="/api-reference/payment-apis/troubleshooting">
    Common issues and solutions for the Sandbox environment
  </Card>
</CardGroup>

