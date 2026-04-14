# Confirm authentication
npx awal@latest status
```

## CLI commands

| Command                                      | Purpose                                |
| -------------------------------------------- | -------------------------------------- |
| `npx awal@latest status`                     | Check server health and auth status    |
| `npx awal@latest auth login <email>`         | Send OTP code to email, returns flowId |
| `npx awal@latest auth verify <flowId> <otp>` | Complete authentication with OTP code  |
| `npx awal@latest balance`                    | Get USDC wallet balance                |
| `npx awal@latest address`                    | Get wallet address                     |
| `npx awal@latest show`                       | Open the wallet companion window       |

## JSON output

All commands support `--json` for machine-readable output:

```bash theme={null}
npx awal@latest status --json
npx awal@latest auth login user@example.com --json
npx awal@latest auth verify <flowId> <otp> --json
```

