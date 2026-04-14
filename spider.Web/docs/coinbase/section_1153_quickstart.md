# Quickstart
Source: https://docs.cdp.coinbase.com/get-started/tools/cdp-cli-quickstart

Install the CDP CLI, configure API keys, and send a testnet transaction in minutes.

<Tip>
  **Using an AI agent?** Point the assistant at the onboarding skill instead. It handles installation, configuration, and verification: `docs.cdp.coinbase.com/cdp-cli/skill.md`
</Tip>

## Prerequisites

1. Install the CLI (requires Node.js 22+):

   ```bash theme={null}
   npm install -g @coinbase/cdp-cli
   ```

2. Go to [API Keys](https://portal.cdp.coinbase.com/projects/api-keys) in the CDP Portal. Sign in (a project is auto-created on first sign-in).

3. Click **Create API Key** → download the JSON key file. The key secret is only shown at creation time.

## 1. Configure the environment

```bash theme={null}