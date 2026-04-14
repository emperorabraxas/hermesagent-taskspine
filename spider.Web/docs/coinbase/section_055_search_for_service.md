# Search for Service
Source: https://docs.cdp.coinbase.com/agentic-wallet/skills/search-for-service



## Overview

Search and browse the x402 bazaar marketplace for paid API services. Use when you or the user want to find available services, discover APIs, or need an external service to accomplish a task.

No authentication or balance is required for searching.

## Commands

### Search the bazaar

Find paid services by keyword:

```bash theme={null}
npx awal@latest x402 bazaar search <query> [-k <n>] [--force-refresh] [--json]
```

| Option            | Description                          |
| ----------------- | ------------------------------------ |
| `-k, --top <n>`   | Number of results (default: 5)       |
| `--force-refresh` | Re-fetch resource index from CDP API |
| `--json`          | Output as JSON                       |

Results are cached locally at `~/.config/awal/bazaar/` and auto-refresh after 12 hours.

### List bazaar resources

Browse all available resources:

```bash theme={null}
npx awal@latest x402 bazaar list [--network <network>] [--full] [--json]
```

| Option             | Description                             |
| ------------------ | --------------------------------------- |
| `--network <name>` | Filter by network (base, base-sepolia)  |
| `--full`           | Show complete details including schemas |
| `--json`           | Output as JSON                          |

### Inspect payment requirements

Check an endpoint's x402 payment requirements without paying:

```bash theme={null}
npx awal@latest x402 details <url> [--json]
```

Auto-detects the correct HTTP method by trying each until it gets a 402 response, then displays price, accepted payment schemes, network, and input/output schemas.

## Examples

```bash theme={null}