# Sandbox Quickstart
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/sandbox/quickstart

Set up your API keys, create a funded account, and verify your Sandbox environment

**Base URL:** `https://sandbox.cdp.coinbase.com`

## Prerequisites

Before you begin, make sure you have:

* A CDP account with access to the [CDP Portal](https://portal.cdp.coinbase.com)
* A terminal with [cdpcurl](https://github.com/coinbase/cdpcurl) installed (or Postman)

## 1. Create Sandbox API keys

<Steps>
  <Step title="Access CDP Portal Sandbox">
    Navigate to the [CDP Portal Sandbox](https://portal.cdp.coinbase.com/v2/sandbox)
  </Step>

  <Step title="Select your project">
    Choose the project you want to create Sandbox credentials for
  </Step>

  <Step title="Create Sandbox API key">
    * Go to **API Keys** section
    * Click **Create API Key**
    * Select **Sandbox** as the environment
    * Choose appropriate permissions (Accounts, Transfers, Payment Methods, etc.)
    * **Download the API key JSON file** and save it securely
  </Step>
</Steps>

<Warning>
  **Important**:

  * Never commit API keys to version control. Store them securely in environment variables or a secrets manager.
  * Do not use real personal data in the Sandbox environment.
</Warning>

## 2. Install `cdpcurl`

[cdpcurl](https://github.com/coinbase/cdpcurl) is a command-line tool that handles JWT authentication automatically—just point it at your downloaded API key file and it takes care of signing requests for you.

**Install via Homebrew:**

```bash theme={null}
brew tap coinbase/cdpcurl    # Add the CDP tap to Homebrew
brew install cdpcurl          # Install the tool
```

**Or install via Go:**

```bash theme={null}
go install github.com/coinbase/cdpcurl@latest
```

**Set your API key path:**

```bash theme={null}
export CDP_API_KEY=~/Downloads/cdp_api_key.json
```

This lets you use `$CDP_API_KEY` in all commands instead of typing the full path each time.

## 3. Create and fund an account

Create a Sandbox account and add test balances through the Portal UI:

<Steps>
  <Step title="Access your account">
    Navigate to [Portal Accounts](https://portal.cdp.coinbase.com/v2/sandbox) in Sandbox
  </Step>

  <Step title="Create account">
    Name the account (e.g., "My Test Account")
  </Step>

  <Step title="Edit test assets">
    Add a balance to your account. Currently we support USD, USDC, USDT (e.g., set USD to \$1000)
  </Step>
</Steps>

<Frame>
  <img alt="Sandbox account showing test balances for USD, USDT, and USDC" />
</Frame>

<Warning>
  All balances are simulated within the Sandbox environment—no blockchain or testnet connectivity. You cannot fund accounts by sending real or testnet crypto.
</Warning>

## 4. Verify balance(s)

Run the following to verify your account balance:

```bash theme={null}
cdpcurl -k $CDP_API_KEY \
  'https://sandbox.cdp.coinbase.com/platform/v2/accounts/YOUR_ACCOUNT_ID' | sed '1d' | jq
```

<Tip>
  List all your accountIDs:

  ```bash theme={null}
  cdpcurl -k $CDP_API_KEY \
    'https://sandbox.cdp.coinbase.com/platform/v2/accounts' | sed '1d' | jq -r '.accounts[].accountId'
  ```
</Tip>

## 5. Alternative: Test with Postman

Prefer a GUI? See the [Postman guide](/api-reference/payment-apis/sandbox/postman) for setup instructions.

## Next steps

Now that you're set up, explore the resource guides to test specific features:

<CardGroup>
  <Card title="Payment Methods" icon="credit-card" href="/api-reference/payment-apis/sandbox/guides/payment-methods">
    Test fiat withdrawal flows
  </Card>

  <Card title="Deposit Destinations" icon="arrow-down-to-line" href="/api-reference/payment-apis/sandbox/guides/deposit-destinations">
    Create addresses and simulate incoming deposits
  </Card>

  <Card title="Accounts" icon="wallet" href="/api-reference/payment-apis/sandbox/guides/accounts">
    Create and manage test accounts
  </Card>

  <Card title="Transfers" icon="arrow-right-arrow-left" href="/api-reference/payment-apis/sandbox/guides/transfers">
    Test transfers to crypto addresses and emails
  </Card>
</CardGroup>

## Transitioning to Production

When you're ready to move from Sandbox to Production:

* **Complete integration testing:** Ensure all features work correctly in Sandbox
* **Create Production API keys:** Generate Production credentials in the CDP Portal
* **Update configuration:** Switch from `sandbox.cdp.coinbase.com` to `api.cdp.coinbase.com`
* **Start with small transactions:** Begin with small test transactions to verify everything works
* **Set up monitoring:** Configure alerting for failed transactions and API errors

