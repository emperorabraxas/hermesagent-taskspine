# Embedded Wallet Solana Policies
Source: https://docs.cdp.coinbase.com/embedded-wallets/policies/solana-policies



## Overview

This page provides examples for Solana-based embedded wallet policy configurations. These policies control end-user Solana transaction signing, sending, and message signing.

For general embedded wallet policy concepts, see the [Embedded Wallet Policies Overview](/embedded-wallets/policies/overview).

## Supported operations

| Operation                   | Description                                                          |
| --------------------------- | -------------------------------------------------------------------- |
| `signEndUserSolTransaction` | Governs end-user Solana transaction signing                          |
| `sendEndUserSolTransaction` | Governs end-user Solana transaction signing and sending to a network |
| `signEndUserSolMessage`     | Governs end-user Solana message signing                              |

## Supported criteria by operation

| Criterion       | signEndUserSolTransaction | sendEndUserSolTransaction | signEndUserSolMessage |
| --------------- | :-----------------------: | :-----------------------: | :-------------------: |
| **solAddress**  |             Y             |             Y             |                       |
| **solValue**    |             Y             |             Y             |                       |
| **splAddress**  |             Y             |             Y             |                       |
| **splValue**    |             Y             |             Y             |                       |
| **mintAddress** |             Y             |             Y             |                       |
| **solData**     |             Y             |             Y             |                       |
| **programId**   |             Y             |             Y             |                       |
| **solNetwork**  |                           |             Y             |                       |
| **solMessage**  |                           |                           |           Y           |

## SOL transfer policies

### Address allowlist

Restrict end-user SOL transfers to a set of trusted addresses.

```json end-user-sol-allowlist.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Allow end-user SOL transfers only to trusted addresses",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "solAddress",
          "addresses": [
            "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
            "HpabPRRCFbBKSuJr5PdkVvQc85FyxyTWkFM2obBRSvHT"
          ],
          "operator": "in"
        }
      ]
    }
  ]
}
```

### SOL value limit

Limit end-user SOL transfers to 2 SOL (2,000,000,000 lamports) or less.

```json end-user-sol-value-limit.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Limit end-user SOL transfers to 2 SOL",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "solValue",
          "solValue": "2000000000",
          "operator": "<="
        }
      ]
    }
  ]
}
```

### Address denylist

Block end-user transactions to known malicious addresses.

```json end-user-sol-denylist.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Block end-user transfers to known malicious addresses",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "solAddress",
          "addresses": [
            "MaliciousAddress1111111111111111111111111",
            "ScamAddress111111111111111111111111111111"
          ],
          "operator": "not in"
        }
      ]
    }
  ]
}
```

## SPL token policies

### Restrict by token mint

Only allow end-user transactions involving specific token mints (USDC and USDT in this example).

```json end-user-spl-mint-restriction.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Allow only USDC and USDT transfers for end users",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "mintAddress",
          "addresses": [
            "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
          ],
          "operator": "in"
        }
      ]
    }
  ]
}
```

### SPL token value limit

Limit end-user USDC transfers to 500 USDC (500,000,000 base units with 6 decimals).

```json end-user-spl-value-limit.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Limit end-user USDC transfers to 500 USDC",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "mintAddress",
          "addresses": ["EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"],
          "operator": "in"
        },
        {
          "type": "splValue",
          "splValue": "500000000",
          "operator": "<="
        }
      ]
    }
  ]
}
```

### SPL recipient allowlist

Restrict SPL token transfers to pre-approved recipient token accounts.

```json end-user-spl-recipient-allowlist.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Allowlist SPL token recipients for end users",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "splAddress",
          "addresses": [
            "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
            "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"
          ],
          "operator": "in"
        }
      ]
    }
  ]
}
```

## Network restriction policies

### Restrict to specific networks

Only allow end-user transactions to be sent on mainnet.

```json end-user-sol-network-restriction.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Restrict end-user Solana sends to mainnet only",
  "rules": [
    {
      "action": "accept",
      "operation": "sendEndUserSolTransaction",
      "criteria": [
        {
          "type": "solNetwork",
          "networks": ["solana"],
          "operator": "in"
        }
      ]
    }
  ]
}
```

## Program restriction policies

### Allow specific programs only

Restrict end-user transactions to interact only with the System Program and Token Program.

```json end-user-sol-program-restriction.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Allow end-user interactions with System and Token programs only",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "programId",
          "programIds": [
            "11111111111111111111111111111111",
            "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
          ],
          "operator": "in"
        }
      ]
    }
  ]
}
```

## Message signing policies

### Restrict message content

Only allow end users to sign messages matching a specific pattern.

```json end-user-sol-message.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Only allow signing messages with app prefix",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolMessage",
      "criteria": [
        {
          "type": "solMessage",
          "match": "^MyApp:.*"
        }
      ]
    }
  ]
}
```

## Instruction data policies

For advanced instruction data validation using IDL specifications, the `solData` criterion is fully documented in the [Solana IDL Policies](/server-wallets/v2/using-the-wallet-api/policies/solana-idl-policies) reference — use `signEndUserSolTransaction` or `sendEndUserSolTransaction` as the operation name in place of the examples shown there.

```json end-user-sol-data.json lines wrap theme={null}
{
  "scope": "project",
  "description": "Restrict end-user System Program transfers to 1 SOL max",
  "rules": [
    {
      "action": "accept",
      "operation": "signEndUserSolTransaction",
      "criteria": [
        {
          "type": "solData",
          "idls": ["SystemProgram"],
          "conditions": [
            {
              "instruction": "transfer",
              "params": [
                {
                  "name": "lamports",
                  "operator": "<=",
                  "value": "1000000000"
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

## Key considerations

### Token decimals

When setting token amounts, account for token decimals:

* **SOL**: 9 decimals (1 SOL = 1,000,000,000 lamports)
* **USDC**: 6 decimals (1 USDC = 1,000,000 base units)
* **USDT**: 6 decimals (1 USDT = 1,000,000 base units)

### Common addresses

**Token Mints:**

* **USDC**: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
* **USDT**: `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`
* **Wrapped SOL**: `So11111111111111111111111111111111111111112`

**Programs:**

* **System Program**: `11111111111111111111111111111111`
* **Token Program**: `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
* **Associated Token Program**: `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`

## What to read next

* [**Embedded Wallet Policies Overview**](/embedded-wallets/policies/overview): General concepts
* [**Embedded Wallet EVM Policies**](/embedded-wallets/policies/evm-policies): EVM-specific policy examples
* [**Solana IDL Policies**](/server-wallets/v2/using-the-wallet-api/policies/solana-idl-policies): Advanced instruction data validation with IDLs
* [**Policy Engine**](/policy-engine/overview): How the Policy Engine works across all CDP wallet products
* [**API Reference**](/api-reference/v2/rest-api/policy-engine/list-policies): Policy Engine API reference

