# Trade Tokens
Source: https://docs.cdp.coinbase.com/agentic-wallet/skills/trade



## Overview

Trade tokens on Base network. Use when you or the user want to trade, exchange, buy, sell, or convert between tokens.

## Prerequisites

* Must be authenticated (`npx awal@latest status` to check)
* Wallet must have sufficient balance of the source token

## Confirming wallet status

```bash theme={null}
npx awal@latest status
```

If the wallet is not authenticated, refer to the [authenticate-wallet](/agentic-wallet/skills/authenticate) skill.

## Command syntax

```bash theme={null}
npx awal@latest trade <amount> <from> <to> [options]
```

## Arguments

| Argument | Description                                                    |
| -------- | -------------------------------------------------------------- |
| `amount` | Amount to trade (see Amount Formats below)                     |
| `from`   | Source token: alias (usdc, eth, weth) or contract address      |
| `to`     | Destination token: alias (usdc, eth, weth) or contract address |

## Amount formats

| Format        | Example                | Description                            |
| ------------- | ---------------------- | -------------------------------------- |
| Dollar prefix | `$1.00`, `$0.50`       | USD notation                           |
| Decimal       | `1.0`, `0.50`, `0.001` | Human-readable with decimal point      |
| Whole number  | `5`, `100`             | Interpreted as whole tokens            |
| Atomic units  | `500000`               | Large integers treated as atomic units |

<Note>
  Large integers (>100) without a decimal point are treated as atomic units. For example, `500000` for USDC (6 decimals) = \$0.50.
</Note>

## Options

| Option               | Description                                   |
| -------------------- | --------------------------------------------- |
| `-s, --slippage <n>` | Slippage tolerance in basis points (100 = 1%) |
| `--json`             | Output result as JSON                         |

<Note>
  Trading is only available on Base mainnet. Testnet trading is not currently supported.
</Note>

## Token aliases

| Alias | Token | Decimals | Address                                    |
| ----- | ----- | -------- | ------------------------------------------ |
| usdc  | USDC  | 6        | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| eth   | ETH   | 18       | 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE |
| weth  | WETH  | 18       | 0x4200000000000000000000000000000000000006 |

## Examples

```bash theme={null}