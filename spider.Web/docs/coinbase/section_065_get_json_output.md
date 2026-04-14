# Get JSON output
npx awal@latest send 1 vitalik.eth --json
```

## ENS resolution

ENS names are automatically resolved to addresses via Ethereum mainnet. The command will:

1. Detect ENS names (any string containing a dot that isn't a hex address)
2. Resolve the name to an address
3. Display both the ENS name and resolved address in the output

## Error handling

| Error                        | Resolution                                                   |
| ---------------------------- | ------------------------------------------------------------ |
| "Not authenticated"          | Run `npx awal@latest auth login <email>` first               |
| "Insufficient balance"       | Check balance with `npx awal@latest balance` and fund wallet |
| "Could not resolve ENS name" | Verify the ENS name exists                                   |
| "Invalid recipient"          | Must be valid 0x address or ENS name                         |

