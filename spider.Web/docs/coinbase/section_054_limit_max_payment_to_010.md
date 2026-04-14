# Limit max payment to $0.10
npx awal@latest x402 pay https://example.com/api/data --max-amount 100000
```

## Error handling

| Error                                | Resolution                                                                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| "Not authenticated"                  | Run `npx awal@latest auth login <email>` first                                                                               |
| "No X402 payment requirements found" | URL may not be an x402 endpoint; use [search-for-service](/agentic-wallet/skills/search-for-service) to find valid endpoints |
| "Insufficient balance"               | Fund wallet with USDC; see [fund](/agentic-wallet/skills/fund) skill                                                         |

