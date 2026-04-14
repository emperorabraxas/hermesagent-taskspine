# Embedded Wallet EVM Policies
Source: https://docs.cdp.coinbase.com/embedded-wallets/policies/evm-policies



## Overview

This page provides examples for EVM-based embedded wallet policy configurations. These policies control end-user EVM transaction signing, sending, message signing, and typed data signing.

For general embedded wallet policy concepts, see the [Embedded Wallet Policies Overview](/embedded-wallets/policies/overview).

## Supported operations

| Operation                   | Description                                                       |
| --------------------------- | ----------------------------------------------------------------- |
| `signEndUserEvmTransaction` | Governs end-user EVM transaction signing                          |
| `sendEndUserEvmTransaction` | Governs end-user EVM transaction signing and sending to a network |
| `signEndUserEvmMessage`     | Governs end-user EIP-191 message signing                          |
| `signEndUserEvmTypedData`   | Governs end-user EIP-712 typed data signing                       |

## Supported criteria by operation

| Criterion                         | signEndUserEvmTransaction | sendEndUserEvmTransaction | signEndUserEvmMessage | signEndUserEvmTypedData |
| --------------------------------- | :-----------------------: | :-----------------------: | :-------------------: | :---------------------: |
| **ethValue**                      |             Y             |             Y             |                       |                         |
| **evmAddress**                    |             Y             |             Y             |                       |                         |
| **evmData**                       |             Y             |             Y             |                       |                         |
| **netUSDChange**                  |             Y             |             Y             |                       |                         |
| **evmNetwork**                    |                           |             Y             |                       |                         |
| **evmMessage**                    |                           |                           |           Y           |                         |
| **evmTypedDataField**             |                           |                           |                       |            Y            |
| **evmTypedDataVerifyingContract** |                           |                           |                       |            Y            |

## Transaction policies

### Allowlist

Allow end-user transaction signing only to specific addresses.

```json end-user-evm-allowlist.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Allow end-user signing only to approved addresses",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserEvmTransaction",
      "criteria": [
        {
          "type": "evmAddress",
          "addresses": [
            "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "0x000000000000000000000000000000000000dEaD"
          ],
          "operator": "in"
        }
      ]
    }
  ]
}
```

### Denylist

Block end-user transaction signing to known risky addresses.

```json end-user-evm-denylist.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Block end-user signing to known risky addresses",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserEvmTransaction",
      "criteria": [
        {
          "type": "evmAddress",
          "addresses": [
            "0xffffffffffffffffffffffffffffffffffffffff"
          ],
          "operator": "not in"
        }
      ]
    }
  ]
}
```

### Transaction value limit

Limit end-user transactions to 1 ETH or less.

```json end-user-evm-value-limit.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Limit end-user transactions to 1 ETH",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserEvmTransaction",
      "criteria": [
        {
          "type": "ethValue",
          "ethValue": "1000000000000000000",
          "operator": "<="
        }
      ]
    }
  ]
}
```

### USD spend limit

Limit end-user transactions to \$100 USD or less in total asset exposure.

<Note>The `netUSDChange` criterion is only evaluated for mainnet transactions and is ignored for testnet.</Note>

```json end-user-evm-usd-limit.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Limit end-user transactions to $100 USD",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserEvmTransaction",
      "criteria": [
        {
          "type": "netUSDChange",
          "changeCents": 10000,
          "operator": "<="
        }
      ]
    },
    {
      "action": "accept",
      "operation": "sendEndUserEvmTransaction",
      "criteria": [
        {
          "type": "netUSDChange",
          "changeCents": 10000,
          "operator": "<="
        }
      ]
    }
  ]
}
```

### Network restriction

Restrict end-user transactions to specific networks.

```json end-user-evm-network-restriction.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Restrict end-user sends to Base and Ethereum only",
  "rules": [
    {
      "action": "accept",
      "operation": "sendEndUserEvmTransaction",
      "criteria": [
        {
          "type": "evmNetwork",
          "networks": ["base", "ethereum"],
          "operator": "in"
        }
      ]
    }
  ]
}
```

### Contract interaction restriction

Restrict end-user transactions to specific contract functions using the `evmData` criterion.

```json end-user-evm-contract-restriction.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Allow end-user USDC transfers up to 10,000 tokens on Base",
  "rules": [
    {
      "action": "accept",
      "operation": "sendEndUserEvmTransaction",
      "criteria": [
        {
          "type": "evmNetwork",
          "networks": ["base"],
          "operator": "in"
        },
        {
          "type": "evmAddress",
          "addresses": ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
          "operator": "in"
        },
        {
          "type": "evmData",
          "abi": "erc20",
          "conditions": [
            {
              "function": "transfer",
              "params": [
                {
                  "name": "value",
                  "operator": "<=",
                  "value": "10000000000"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Message signing policies

### Restrict message content

Ensure end users can only sign messages matching a specific pattern.

```json end-user-evm-message.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Only allow signing messages with app prefix",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserEvmMessage",
      "criteria": [
        {
          "type": "evmMessage",
          "match": "^MyApp:.*"
        }
      ]
    }
  ]
}
```

## Typed data policies

### Restrict verifying contract

Only allow end users to sign typed data for specific verifying contracts.

```json end-user-evm-typed-data.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Only allow typed data signing for approved contracts",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserEvmTypedData",
      "criteria": [
        {
          "type": "evmTypedDataVerifyingContract",
          "addresses": [
            "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
          ],
          "operator": "in"
        }
      ]
    }
  ]
}
```

### Restrict typed data fields

Validate specific fields within the typed data structure.

```json end-user-evm-typed-data-fields.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Restrict Payment typed data to approved recipients under $100",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserEvmTypedData",
      "criteria": [
        {
          "type": "evmTypedDataField",
          "types": {
            "primaryType": "Payment",
            "types": {
              "EIP712Domain": [
                { "name": "name", "type": "string" },
                { "name": "version", "type": "string" },
                { "name": "chainId", "type": "uint256" },
                { "name": "verifyingContract", "type": "address" }
              ],
              "Payment": [
                { "name": "to", "type": "address" },
                { "name": "amount", "type": "uint256" }
              ]
            }
          },
          "conditions": [
            {
              "path": "to",
              "operator": "in",
              "addresses": [
                "0x000000000000000000000000000000000000dEaD"
              ]
            },
            {
              "path": "amount",
              "operator": "<=",
              "value": "100000000"
            }
          ]
        }
      ]
    }
  ]
}
```

## What to read next

* [**Embedded Wallet Policies Overview**](/embedded-wallets/policies/overview): General concepts
* [**Embedded Wallet Solana Policies**](/embedded-wallets/policies/solana-policies): Solana-specific policy examples
* [**Policy Engine**](/policy-engine/overview): How the Policy Engine works across all CDP wallet products
* [**API Reference**](/api-reference/v2/rest-api/policy-engine/list-policies): Policy Engine API reference

