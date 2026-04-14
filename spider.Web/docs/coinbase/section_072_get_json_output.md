# Get JSON output
npx awal@latest trade $1 usdc eth --json
```

## Error handling

| Error                                             | Resolution                                        |
| ------------------------------------------------- | ------------------------------------------------- |
| "Not authenticated"                               | Run `npx awal@latest auth login <email>` first    |
| "Invalid token"                                   | Use a valid alias (usdc, eth, weth) or 0x address |
| "Cannot trade a token to itself"                  | From and to must be different                     |
| "Trade failed: TRANSFER\_FROM\_FAILED"            | Insufficient balance or approval issue            |
| "No liquidity"                                    | Try a smaller amount or different token pair      |
| "Amount has X decimals but token only supports Y" | Too many decimal places                           |

