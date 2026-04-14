# Upgrading to Webhooks v2
Source: https://docs.cdp.coinbase.com/data/webhooks/v2-upgrade



## Overview

This guide outlines the steps to upgrade from Webhooks v1 to v2. Webhooks v1 will be deprecated on January 26th, 2026.

Upgrade is designed to be seamless and instant. The primary change developers must make is modifying their codebases to accept the new v2 payload structure and updating their signature verification method.

## How to Upgrade

<Steps>
  <Step title="Upgrade in CDP Portal">
    Migrating your webhook endpoints from v1 to v2 is an automatic process initiated from your developer portal.

    1. Navigate to the [CDP Portal Webhooks page](https://portal.cdp.coinbase.com/products/data/webhooks)
    2. Click **Upgrade** on each v1 webhook you wish to migrate
    3. Upgrade will happen automatically. Your endpoint will begin receiving v2 payloads immediately.

    <Note>
      If your v1 webhook monitors multiple contract addresses, the upgrade will automatically create a separate v2 subscription for each contract address. For example, a v1 webhook with 3 contracts will upgrade to 3 individual v2 subscriptions.
    </Note>
  </Step>

  <Step title="Update payload handling">
    Your webhook handler must be updated to parse the new v2 event structure. Below is an example of the v2 payload:

    ```json title="v2-payload-example.json" theme={null}
    {
      "block_number": 38218578,
      "contract_address": "0x125E6687d4313864e53df431d5425969c15Eb2F",
      "event_name": "Transfer",
      "event_signature": "Transfer(address,address,uint256)",
      "log_index": 755,
      "network": "base-mainnet",
      "parameters": {
        "from": "0x0000000005f122FDDe066942195c10106d490486",
        "to": "0x0000000000000000000000000000000000000000",
        "value": "637064239"
      },
      "timestamp": "2025-11-15T17:08:24Z",
      "transaction_from": "0x0000000005f122FDDe066942195c10106d490486",
      "transaction_hash": "0xf1bdb4c4c48dd1c3c43b720890200f4d5a170c856b5c01ad1ab14e69ec",
      "transaction_to": "0x0000000005f122FDDe066942195c10106d490486"
    }
    ```

    All V2 webhooks include  the `block_number`, `timestamp`, `transaction_hash` and `network` fields, as well as event-specific parameters
  </Step>

  <Step title="Update signature verification">
    Alongside the payload change, you must update your signature verification logic to be compatible with v2.

    Follow the [Verify Signatures guide](/data/webhooks/verify-signatures) for a complete, step-by-step implementation of the new v2 verification logic.
  </Step>
</Steps>

## What to read next

* **[Verify webhook signatures](/data/webhooks/verify-signatures)**: Learn how to verify webhook signatures to ensure events are coming from Coinbase
* **[Webhooks Quickstart](/data/webhooks/quickstart)**: Get started with creating new webhook subscriptions

## Support and feedback

* **[CDP Discord](https://discord.com/channels/1220414409550336183/1235304277904199750)**: Join #onchain-data for help and community support

