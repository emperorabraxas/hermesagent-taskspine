# Sandbox Environment
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/sandbox

Test your CDP Payments API integration safely using the sandbox environment

## Overview

The CDP Payments API sandbox environment provides a safe, isolated testing space where you can develop and test your payment integrations without affecting production data or processing real transactions. The sandbox mirrors production functionality while using test data and simulated payment flows.

<Info>
  All API endpoints, authentication methods, and response formats in sandbox are identical to production, making it easy to transition your code when ready.
</Info>

## Key Differences: Sandbox vs Production

| Feature              | Sandbox                      | Production                 |
| -------------------- | ---------------------------- | -------------------------- |
| **API Endpoint**     | `sandbox.cdp.coinbase.com`   | `api.cdp.coinbase.com`     |
| **API Keys**         | Sandbox-specific credentials | Production credentials     |
| **Transactions**     | Simulated (no real value)    | Real payment processing    |
| **Test Accounts**    | Unlimited test accounts      | Real user accounts         |
| **Rate Limits**      | Same as production           | Standard production limits |
| **Data Persistence** | Permanent                    | Permanent                  |
| **Webhooks**         | Supported                    | Supported                  |

## Getting Started

### 1. Create Sandbox API Credentials

To access the sandbox environment, you'll need to create sandbox-specific API credentials:

<Steps>
  <Step title="Access CDP Portal">
    Navigate to the [CDP Portal](https://portal.cdp.coinbase.com/)
  </Step>

  <Step title="Select Your Project">
    Choose the project you want to create sandbox credentials for
  </Step>

  <Step title="Create Sandbox API Key">
    * Go to **API Keys** section
    * Click **Create API Key**
    * Select **Sandbox** as the environment
    * Choose appropriate permissions (Accounts, Transfers, Payment Methods, etc.)
    * Save your API key name and private key securely
  </Step>

  <Step title="Configure Your Application">
    Update your application to use the sandbox endpoint and credentials
  </Step>
</Steps>

<Warning>
  **Important**:

  * Never commit API keys to version control. Store them securely in environment variables or a secrets manager.
  * Real personal data must **not** be used in the sandbox environment.
</Warning>

### 2. Testing Workflows

Use following Postman Collection and Environment with the key created in previous step to test CDP Sandbox.

* <a href="/api-reference/payment-apis/CDP Payments Sandbox.postman_collection-docs.json">CDP Payments - Postman Collection</a>
* <a href="/api-reference/payment-apis/CDP Payments Sandbox.postman_environment-docs.json">CDP Payments - Postman Environment</a>

## Best Practices

<AccordionGroup>
  <Accordion title="Isolate Sandbox Configuration">
    Keep sandbox configuration completely separate from production:

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

  <Accordion title="Test Error Handling">
    Use sandbox to thoroughly test error scenarios:

    * Invalid authentication
    * Malformed requests
    * Rate limiting
    * Network timeouts
    * Insufficient funds
    * Invalid account details
  </Accordion>

  <Accordion title="Automate Integration Tests">
    Create automated test suites that run against sandbox:

    ```typescript theme={null}
    // tests/integration/payments.test.ts
    describe('Payments API Integration', () => {
      beforeAll(() => {
        // Set up sandbox client
      });
      
      test('should create account', async () => {
        const account = await createAccount({
          name: 'Test Account',
          currency: 'USD'
        });
        
        expect(account.id).toBeDefined();
        expect(account.currency).toBe('USD');
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

  <Accordion title="Monitor API Usage">
    Track your API usage patterns in sandbox to understand production requirements:

    * Request volumes
    * Response times
    * Error rates
    * Rate limit consumption
  </Accordion>
</AccordionGroup>

## Test data for transfers

When testing email-based transfers in the sandbox environment, only specific whitelisted email addresses will return successful validation responses. This approach prevents privacy concerns while providing predictable test behavior.

### Whitelisted email addresses

The following email addresses are whitelisted for sandbox testing and will return a `2xx` success response when used as transfer targets:

| Test Email             | Description                   |
| ---------------------- | ----------------------------- |
| `testuser1@domain.com` | Returns successful validation |
| `testuser2@domain.com` | Returns successful validation |

A request body that tests email validation might look like the following:

```json theme={null}
{
  "source": {
    "accountId": "{{accountId}}",
    "asset": "USD"
  },
  "target": {
    "email": "testuser1@domain.com",
    "asset": "USD"
  },
  "amount": "10",
  "validateOnly": true
}
```

<Note>
  Use [`validateOnly: true`](/api-reference/payment-apis/rest-api/transfers/transfers#transfer-validation) to test email validation without initiating a transfer.
</Note>

### Non-whitelisted emails

Any email address **not** in the whitelist will return a `4xx` validation error indicating the user was not found.

<Warning>
  In production, transfers validate against actual Coinbase user accounts. The sandbox whitelist is intentionally limited to prevent privacy concerns around validating real email addresses.
</Warning>

### Reserved email addresses for simulated outcomes

When testing email-based transfers in the sandbox environment, you can use the following reserved email address to simulate a deterministic error outcome.

| Reserved Email                    | Simulated Outcome    |
| --------------------------------- | -------------------- |
| `sandboxinvalidtarget@domain.com` | Invalid email target |

#### Sample request and response payload

Request payload:

```json lines wrap theme={null}
{
  "source": {
    "accountId": "{{accountId}}",
    "asset": "usdc"
  },
  "target": {
    "email": "sandboxinvalidtarget@domain.com",
    "asset": "usdc"
  },
  "amount": "10",
  "asset": "usdc",
  "execute": true
}
```

Expected response: HTTP `400`

```json lines wrap theme={null}
{
    "correlationId": "90d67ad3-d067-41d8-816f-10f3a0144502",
    "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid-request",
    "errorMessage": "Target email is invalid.",
    "errorType": "invalid_request"
}
```

### Reserved onchain addresses for simulated outcomes

When testing onchain transfers in the sandbox environment, you can use reserved onchain addresses to simulate deterministic success or failure outcomes. Each address returns a predictable response based on the address used.

<Warning>
  These reserved addresses are for **testing purposes** in the sandbox environment. In production, they are valid onchain addresses and any funds sent to them **will be lost**.
</Warning>

| Reserved Address                             | Simulated Outcome       |
| -------------------------------------------- | ----------------------- |
| `0x1111111111111111111111111111111111111111` | Success                 |
| `0x2222222222222222222222222222222222222222` | Transfer invalid target |
| `0x3333333333333333333333333333333333333333` | Invalid address         |
| `0x4444444444444444444444444444444444444444` | Unsupported network     |

#### Sample request and response payloads

<Tabs>
  <Tab title="Success">
    Request payload:

    ```json lines wrap theme={null}
    {
      "source": {
        "accountId": "{{accountId}}",
        "asset": "usdc"
      },
      "target": {
        "network": "base",
        "address": "0x1111111111111111111111111111111111111111",
        "asset": "usdc"
      },
      "amount": "5.00",
      "asset": "usdc",
      "execute": true
    }
    ```

    Expected response: HTTP `2xx` with a normal transfer response.
  </Tab>

  <Tab title="Transfer invalid target">
    Request payload:

    ```json lines wrap theme={null}
    {
      "source": {
        "accountId": "{{accountId}}",
        "asset": "usdc"
      },
      "target": {
        "network": "base",
        "address": "0x2222222222222222222222222222222222222222",
        "asset": "usdc"
      },
      "amount": "5.00",
      "asset": "usdc",
      "execute": true
    }
    ```

    Expected response: HTTP `400`

    ```json lines wrap theme={null}
    {
      "errorType": "invalid_request",
      "errorMessage": "'target' is invalid: must match one of [Account, Payment Method, Onchain Address, Email Instrument]. Account requires 'accountId'; Payment Method requires 'paymentMethodId'; Onchain Address requires 'network'; Email Instrument requires 'email'"
    }
    ```
  </Tab>

  <Tab title="Invalid address">
    Request payload:

    ```json lines wrap theme={null}
    {
      "source": {
        "accountId": "{{accountId}}",
        "asset": "usdc"
      },
      "target": {
        "network": "base",
        "address": "0x3333333333333333333333333333333333333333",
        "asset": "usdc"
      },
      "amount": "5.00",
      "asset": "usdc",
      "execute": true
    }
    ```

    Expected response: HTTP `400`

    ```json lines wrap theme={null}
    {
      "errorType": "invalid_request",
      "errorMessage": "Invalid onchain address for network base."
    }
    ```
  </Tab>

  <Tab title="Unsupported network">
    Request payload:

    ```json lines wrap theme={null}
    {
      "source": {
        "accountId": "{{accountId}}",
        "asset": "usdc"
      },
      "target": {
        "network": "base",
        "address": "0x4444444444444444444444444444444444444444",
        "asset": "usdc"
      },
      "amount": "5.00",
      "asset": "usdc",
      "execute": true
    }
    ```

    Expected response: HTTP `400`

    ```json lines wrap theme={null}
    {
      "errorType": "invalid_request",
      "errorMessage": "base is not a supported network."
    }
    ```
  </Tab>
</Tabs>

## Limitations & Considerations

<Warning>
  Be aware of these sandbox limitations when testing:
</Warning>

* **Performance**: Response times may vary from production
* **Third-Party Services**: Some third-party integrations use mocked responses
* **Rate Limits**: Same rate limits as production apply to prevent abuse
* **Compliance Checks**: Simplified compliance flows (no real KYC/AML)

## Transitioning to Production

When you're ready to move from sandbox to production:

<Steps>
  <Step title="Complete Integration Testing">
    Ensure all features work correctly in sandbox with comprehensive test coverage
  </Step>

  <Step title="Review Security Practices">
    * Ensure API keys are stored securely
    * Review access control and permissions
    * Implement proper error handling
  </Step>

  <Step title="Create Production API Keys">
    Generate production credentials in the CDP Portal with appropriate permissions
  </Step>

  <Step title="Update Configuration">
    Switch from sandbox to production endpoints:

    ```diff theme={null}
    - baseURL: 'https://sandbox.cdp.coinbase.com'
    + baseURL: 'https://api.cdp.coinbase.com'
    ```
  </Step>

  <Step title="Start with Small Transactions">
    Begin with small test transactions to verify everything works as expected
  </Step>

  <Step title="Monitor Closely">
    Set up monitoring and alerting for:

    * Failed transactions
    * API errors
    * Unusual activity
  </Step>

  <Step title="Have a Rollback Plan">
    Be prepared to quickly revert to previous code if issues arise
  </Step>
</Steps>

## Need Help?

If you encounter issues with the sandbox environment, see the [Troubleshooting](/api-reference/payment-apis/troubleshooting) page for common issues and solutions.

