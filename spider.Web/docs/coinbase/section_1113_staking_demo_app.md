# Staking demo app
Source: https://docs.cdp.coinbase.com/get-started/demo-apps/starter/staking-demo-app



<LearnButtons />

<Tags />

<Frame>
  <img />
</Frame>

## Coinbase Staking Demo

This repository is an example of how to stake from any Solana wallet in minutes. This codebase uses the [CDP Golang SDK](https://github.com/coinbase/coinbase-sdk-go).

Please check out [our docs](/staking/staking-api/introduction/welcome) to learn more! Also check out our [demo video](https://www.loom.com/share/1be3b9bb536d4edead9345b841d1fee4) of this repository for more details!

> **NOTE: This example is for demonstration purposes only.**
> Make sure to persist your private keys in a secure fashion.

**In production, you should [IP whitelist your API key](/get-started/authentication/security-best-practices) for increased security.**

## Feature requests

If there is specific functionality you'd like to see in the CDP Staking API that is missing, we would love your feedback!

The best way to contact us is in the **#staking** channel of the [CDP Discord](https://discord.com/invite/cdp).

## Set Up

1. Clone this repository:

   ```bash theme={null}
   git clone https://github.com/ProfMoo/coinbase-staking-demo
   ```

2. Provision a [CDP API Key](/get-started/authentication/cdp-api-keys).

3. Set the following environment variables via an `export` shell command:

   ```bash theme={null}
   export CDP_API_KEY_PATH="<path_to_my_cdp_key>"
   export SOLANA_PRIVATE_KEY_PATH="<path_to_my_solana_private_key>"
   export SOLANA_ADDRESS="<my_solana_wallet>"
   ```

4. Run the example application:

   ```bash theme={null}
   go mod tidy && go run main.go
   ```

