# Track CDP Server Wallet Activity
Source: https://docs.cdp.coinbase.com/server-wallets/v2/using-the-wallet-api/webhooks



## Overview

This guide shows how to use [Onchain Data Webhooks](/data/webhooks/overview) from a Server Wallet workflow to create webhook subscriptions via our [REST endpoints](/api-reference/v2/rest-api/webhooks/webhooks) and receive events at your target destination.

<Info>
  Enhanced webhooks for Server Wallets and Embedded Wallets are coming soon. Today, this guide uses Onchain Data webhooks with wallet address filters.
</Info>

<Warning>
  Both `onchain.activity.detected` and `wallet.activity.detected` cover **ERC-20 token transfers only**. Native ETH transactions are a different event stream and are not currently supported. Do not expect ETH transfer notifications from these subscription types.
</Warning>

This is a Server Wallet-focused adaptation of the [Onchain Data Webhooks](/data/webhooks/overview) flow, tailored for use cases such as tracking USDC transfers into and out of wallet addresses.

## Prerequisites

Before setting up your webhook subscription, make sure you have the following:

<AccordionGroup>
  <Accordion title="A Secret API Key">
    Sign up at [portal.cdp.coinbase.com](https://portal.cdp.coinbase.com), then navigate to [API Keys](https://portal.cdp.coinbase.com/projects/api-keys) and select **Create API key** under the **Secret API Keys** tab.

    1. Enter an API key nickname (restrictions are optional)
    2. Click **Create**
    3. Secure your API Key ID and Secret in a safe location
  </Accordion>

  <Accordion title="A webhook URL">
    You'll need an HTTPS URL to receive webhook events. For quick testing, [webhook.site](https://webhook.site) gives free temporary URLs instantly.

    For production, use your own HTTPS endpoint.
  </Accordion>

  <Accordion title="cdpcurl">
    Install `cdpcurl` to make authenticated requests to CDP APIs:

    ```bash theme={null}
    # With Homebrew
    brew tap coinbase/cdpcurl && brew install cdpcurl

    # Or with Go
    go install github.com/coinbase/cdpcurl@latest
    ```
  </Accordion>
</AccordionGroup>

<AccordionGroup>
  <Accordion title="A CDP Server Wallet address">
    If you don't already have one, follow the [Server Wallet v2 Quickstart](/server-wallets/v2/introduction/quickstart).

    After completing it, you should have an EVM wallet address to use as `WALLET_ADDRESS`.

    <Note>
      Funding is not required to create a webhook subscription. Funding is required only if you want to trigger and validate live transfer events.
    </Note>
  </Accordion>

  <Accordion title="Local environment variables configured">
    Set these once in your terminal so you can run the commands in this guide as-is.
    This guide defaults to Base Sepolia for testnet validation.

    ```bash theme={null}
    export CDP_API_KEY_ID="YOUR_API_KEY_ID" # auth cdpcurl requests
    export CDP_API_KEY_SECRET="YOUR_API_KEY_SECRET" # auth cdpcurl requests
    export WEBHOOK_URL="https://webhook.site/YOUR_UNIQUE_ID" # i.e. webhook.site
    export WALLET_ADDRESS="0xYourServerWalletAddress" # your CDP wallet address
    export NETWORK="base-sepolia" # testnet before going live
    export USDC_CONTRACT_ADDRESS="0x036CbD53842c5426634e7929541eC2318f3dCF7e" # USDC on Base Sepolia
    ```

    <Note>
      `USDC_CONTRACT_ADDRESS` tells the webhook which token contract to watch. Without this filter, your subscription may match transfers from other tokens too. The value shown above is the USDC contract on Base Sepolia (testnet).
    </Note>

    <Tip>
      If you downloaded your Secret API key file (`cdp_api_key.json`) from CDP Portal, you can load credentials directly:

      ```bash theme={null}
      export CDP_API_KEY_ID="$(jq -r '.id // .name' "$HOME/Downloads/cdp_api_key.json")"
      export CDP_API_KEY_SECRET="$(jq -r '.privateKey' "$HOME/Downloads/cdp_api_key.json")"
      ```

      ```bash theme={null}
      brew install jq
      ```
    </Tip>
  </Accordion>
</AccordionGroup>

## 1. Prepare subscription payload

In this example, you will track USDC transfers in or out of your CDP Server Wallet.

Each subscription listens for `onchain.activity.detected` events on the USDC contract, filtered by your wallet address using the `params.from` and `params.to` labels.

<Tabs>
  <Tab title="Outgoing transfers">
    Run this to create `outgoing-usdc.json` using your exported env vars:

    ```bash theme={null}
    cat > outgoing-usdc.json << EOF
    {
      "description": "USDC Transfers",
      "eventTypes": ["onchain.activity.detected"],
      "target": {
        "url": "$WEBHOOK_URL",
        "method": "POST"
      },
      "labels": {
        "network": "$NETWORK",
        "contract_address": "$USDC_CONTRACT_ADDRESS",
        "event_name": "Transfer",
        "params.from": "$WALLET_ADDRESS"
      },
      "isEnabled": true
    }
    EOF
    ```
  </Tab>

  <Tab title="Incoming transfers">
    Run this to create `incoming-usdc.json` using your exported env vars:

    ```bash theme={null}
    cat > incoming-usdc.json << EOF
    {
      "description": "USDC Transfers",
      "eventTypes": ["onchain.activity.detected"],
      "target": {
        "url": "$WEBHOOK_URL",
        "method": "POST"
      },
      "labels": {
        "network": "$NETWORK",
        "contract_address": "$USDC_CONTRACT_ADDRESS",
        "event_name": "Transfer",
        "params.to": "$WALLET_ADDRESS"
      },
      "isEnabled": true
    }
    EOF
    ```
  </Tab>
</Tabs>

For all available fields and advanced options, see **[REST API Reference](/api-reference/v2/rest-api/webhooks/create-webhook-subscription)**.

<Note>
  You can filter on any ERC-20 event parameter using `params.[any_param]` in `labels` (e.g. `params.from`, `params.to`, `params.value`). See the [configuration fields table](/data/webhooks/quickstart#configuration-fields) in the Onchain Data Webhooks Quickstart for the full list of supported label filters.
</Note>

<Accordion title="Alternative: monitor all wallet activity with wallet.activity.detected">
  <Warning>
    `wallet.activity.detected` covers ERC-20 token transfers only. Native ETH transfers are a different event stream and are not currently supported. Do not expect ETH transfer notifications from this subscription type.
  </Warning>

  Use this when:

  * You want to track all ERC-20 tokens, not just USDC
  * You don't need contract-level filtering
  * You prefer fewer labels and simpler setup

  ```bash theme={null}
  cat > outgoing-wallet.json << EOF
  {
    "description": "Outgoing transfers",
    "eventTypes": ["wallet.activity.detected"],
    "target": {
      "url": "$WEBHOOK_URL"
    },
    "labels": {
      "params.from": "$WALLET_ADDRESS"
    },
    "isEnabled": true
  }
  EOF

  cat > incoming-wallet.json << EOF
  {
    "description": "Incoming transfers",
    "eventTypes": ["wallet.activity.detected"],
    "target": {
      "url": "$WEBHOOK_URL"
    },
    "labels": {
      "params.to": "$WALLET_ADDRESS"
    },
    "isEnabled": true
  }
  EOF
  ```

  Then create both subscriptions using the same `cdpcurl` commands from step 2, replacing `outgoing-usdc.json` / `incoming-usdc.json` with `outgoing-wallet.json` / `incoming-wallet.json`.
</Accordion>

## 2. Subscribe to transfer events

Using the configurations you created in the previous step, create webhook subscriptions using `cdpcurl`.

<Tabs>
  <Tab title="Outgoing transfers">
    ```bash lines theme={null}
    cdpcurl -X POST \
      -i "$CDP_API_KEY_ID" \
      -s "$CDP_API_KEY_SECRET" \
      "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
      -d "$(cat outgoing-usdc.json)"
    ```
  </Tab>

  <Tab title="Incoming transfers">
    ```bash lines theme={null}
    cdpcurl -X POST \
      -i "$CDP_API_KEY_ID" \
      -s "$CDP_API_KEY_SECRET" \
      "https://api.cdp.coinbase.com/platform/v2/data/webhooks/subscriptions" \
      -d "$(cat incoming-usdc.json)"
    ```
  </Tab>
</Tabs>

You should see a response similar to the following, indicating the subscription was created:

```json title="response.json" theme={null}
201 Created
{
  "createdAt": "2025-10-08T13:58:38.681893Z",
  "description": "USDC Transfers",
  "eventTypes": [
    "onchain.activity.detected"
  ],
  "isEnabled": true,
  "labels": {
    "project": "<YOUR_CDP_PROJECT_ID>",
    "network": "base-sepolia",
    "contract_address": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    "event_name": "Transfer",
    "params.to": "0xYourWalletAddress"
  },
  "metadata": {
    "secret": "<SECRET_FOR_WEBHOOK_VERIFICATION>"
  },
  "subscriptionId": "<YOUR_SUBSCRIPTION_ID>",
  "target": {
    "url": "https://your-webhook-url.com"
  }
}
```

## 3. Verify webhook event capture

Use the CDP Faucet to send 1 USDC to your wallet and confirm the webhook fires.

<Steps>
  <Step title="Send USDC via CDP Faucet">
    Open the [CDP Faucet](https://portal.cdp.coinbase.com/products/faucet?token=USDC\&network=base-sepolia), select **Base Sepolia** + **USDC**, paste your `WALLET_ADDRESS`, and click **Send**.
  </Step>

  <Step title="Check your webhook URL">
    Open your `WEBHOOK_URL` and wait for an incoming `POST` request. You should receive an `onchain.activity.detected` payload similar to:

    ```json theme={null}
    {
      "block_number": 12345678,
      "contract_address": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "event_name": "Transfer",
      "event_signature": "Transfer(address,address,uint256)",
      "network": "base-sepolia",
      "parameters": {
        "from": "0xFaucetAddress",
        "to": "0xYourWalletAddress",
        "value": "1000000"
      },
      "timestamp": "2026-03-04T22:13:42Z",
      "transaction_hash": "0xYourTransactionHash"
    }
    ```
  </Step>

  <Step title="Confirm the event matches your filter">
    Check that `parameters.to` matches your `WALLET_ADDRESS` you exported in the prerequisites. This confirms your subscription to incoming transfer events is working successfully.

    To test outgoing, send USDC **from** your wallet and confirm `parameters.from` matches. See [Transferring tokens from a CDP Wallet](/server-wallets/v2/using-the-wallet-api/transfers).
  </Step>
</Steps>

For managing subscriptions after creation (list, view, update, delete), see the **[REST API Reference](/api-reference/v2/rest-api/webhooks/webhooks)**.

## What to read next

<CardGroup>
  <Card title="Create webhook subscription" icon="webhook" href="/api-reference/v2/rest-api/webhooks/create-webhook-subscription">
    Full reference for supported event types, label filters (`params.*`, `transaction_from`, `transaction_to`), and advanced options
  </Card>

  <Card title="Onchain Data Webhooks Overview" icon="wave-pulse" href="/data/webhooks/overview">
    Learn more about webhook capabilities, delivery guarantees, and supported use cases
  </Card>
</CardGroup>

