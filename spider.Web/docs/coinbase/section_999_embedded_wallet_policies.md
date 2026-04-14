# Embedded Wallet Policies
Source: https://docs.cdp.coinbase.com/embedded-wallets/policies/overview



## Overview

CDP Embedded Wallets support **Policies** that enable developers to govern end-user signing operations. Policies provide flexible configuration for enforcing controls based on transaction parameters such as destination address, transaction value, and operation frequency.

Embedded wallet policies leverage the [Policy Engine](/api-reference/v2/rest-api/policy-engine/list-policies) APIs to govern end-user signing flows, with support for operations like rate limiting.

<Warning>
  Embedded wallet policies only support **project scope**. Account-level policies are not available for embedded wallets.
</Warning>

### Use cases

* **Address allowlists and denylists:** Restrict which addresses end users can transact with
* **Transaction value limits:** Cap the amount of native or token value per transaction
* **Message signing restrictions:** Ensure only messages matching specific patterns can be signed
* **Network restrictions:** Restrict end-user transactions to specific networks
* **Contract interaction controls:** Validate transaction data against contract ABIs or Solana IDLs

## Supported operations

### EVM Operations

* `signEndUserEvmTransaction`: Governs end-user EVM transaction signing
* `sendEndUserEvmTransaction`: Governs end-user EVM transaction signing and sending to a network
* `signEndUserEvmMessage`: Governs end-user [EIP-191](https://eips.ethereum.org/EIPS/eip-191) message signing
* `signEndUserEvmTypedData`: Governs end-user [EIP-712](https://eips.ethereum.org/EIPS/eip-712) typed data signing

### Solana Operations

* `signEndUserSolTransaction`: Governs end-user Solana transaction signing
* `sendEndUserSolTransaction`: Governs end-user Solana transaction signing and broadcast
* `signEndUserSolMessage`: Governs end-user Solana message signing

## Creating an embedded wallet policy

Embedded wallet policies are created using developer-authenticated APIs and the CDP SDK, not the frontend SDKs used for end-user actions.

### Install the CDP SDK

<CodeGroup>
  ```bash npm theme={null}
  npm install @coinbase/cdp-sdk
  ```

  ```bash pip theme={null}
  pip install cdp-sdk
  ```
</CodeGroup>

### Create a policy

<CodeGroup>
  ```ts TypeScript lines wrap theme={null}
  import { CdpClient } from "@coinbase/cdp-sdk";

  const cdp = new CdpClient();

  const policy = await cdp.policies.createPolicy({
    policy: {
      scope: "project",
      description: "Embedded wallet: accept EVM txs to allowlisted addresses",
      rules: [
        {
          action: "accept",
          operation: "signEndUserEvmTransaction",
          criteria: [
            {
              type: "evmAddress",
              addresses: ["0x000000000000000000000000000000000000dEaD"],
              operator: "in",
            },
          ],
        },
      ],
    },
  });

  console.log("Created embedded wallet policy:", policy.id);
  ```

  ```python Python lines wrap theme={null}
  import asyncio
  from cdp import CdpClient

  async def main():
      async with CdpClient() as cdp:
          policy = await cdp.policies.create_policy({
              "scope": "project",
              "description": "Embedded wallet: accept EVM txs to allowlisted addresses",
              "rules": [
                  {
                      "action": "accept",
                      "operation": "signEndUserEvmTransaction",
                      "criteria": [
                          {
                              "type": "evmAddress",
                              "addresses": ["0x000000000000000000000000000000000000dEaD"],
                              "operator": "in",
                          },
                      ],
                  }
              ],
          })
          print(f"Created embedded wallet policy: {policy.id}")

  asyncio.run(main())
  ```
</CodeGroup>

## Policy evaluation

Embedded wallet policies are evaluated **before** any signing operation is executed:

1. Rules are processed in the order they are defined in the `rules` array.
2. If a rule's criteria match (logical AND across all criteria), the rule's `action` (`accept` or `reject`) is applied immediately.
3. If no rule matches, the request is **rejected** (fail-secure default).

Since embedded wallets only support project-scope policies, there is no account-level policy evaluation step.

## What to read next

* [**Embedded Wallet EVM Policies**](/embedded-wallets/policies/evm-policies): EVM-specific policy examples for embedded wallets
* [**Embedded Wallet Solana Policies**](/embedded-wallets/policies/solana-policies): Solana-specific policy examples for embedded wallets
* [**Policy Engine**](/policy-engine/overview): How the Policy Engine works across all CDP wallet products
* [**API Reference**](/api-reference/v2/rest-api/policy-engine/list-policies): Policy Engine API reference

