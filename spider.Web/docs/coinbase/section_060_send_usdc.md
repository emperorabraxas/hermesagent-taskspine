# Send USDC
Source: https://docs.cdp.coinbase.com/agentic-wallet/skills/send



## Overview

Send USDC to an Ethereum address or ENS name. Use when you or the user want to send money, pay someone, transfer USDC, tip, donate, or send funds to a wallet address or .eth name.

## Prerequisites

* Must be authenticated (`npx awal@latest status` to check)
* Wallet must have sufficient USDC balance (`npx awal@latest balance` to check)

## Confirming wallet status

```bash theme={null}
npx awal@latest status
```

If the wallet is not authenticated, refer to the [authenticate-wallet](/agentic-wallet/skills/authenticate) skill.

## Command syntax

```bash theme={null}
npx awal@latest send <amount> <recipient> [--chain <chain>] [--json]
```

## Arguments

| Argument    | Description                                                                                                                   |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `amount`    | Amount to send: `$1.00`, `1.00`, or atomic units (1000000 = \$1). Numbers > 100 without decimals are treated as atomic units. |
| `recipient` | Ethereum address (0x...) or ENS name (vitalik.eth)                                                                            |

## Options

| Option           | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `--chain <name>` | Blockchain network: `base` (default) or `base-sepolia` |
| `--json`         | Output result as JSON                                  |

## Examples

```bash theme={null}