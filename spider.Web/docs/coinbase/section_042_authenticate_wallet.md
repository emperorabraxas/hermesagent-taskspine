# Authenticate Wallet
Source: https://docs.cdp.coinbase.com/agentic-wallet/skills/authenticate



## Overview

Sign in to the wallet via email OTP. Use when you or the user want to log in, sign in, connect, or set up the wallet, or when any wallet operation fails with authentication errors.

This skill is a prerequisite before sending, trading, or funding.

## Authentication flow

Authentication uses a two-step email OTP process.

### 1. Initiate login

```bash theme={null}
npx awal@latest auth login <email>
```

This sends a 6-digit verification code to the email and outputs a `flowId`.

### 2. Verify OTP

```bash theme={null}
npx awal@latest auth verify <flowId> <otp>
```

Use the `flowId` from step 1 and the 6-digit code from the user's email to complete authentication.

<Note>
  If the agent has access to the user's email, it can read the OTP code directly. Otherwise, the agent should ask the user for the code.
</Note>

## Checking authentication status

```bash theme={null}
npx awal@latest status
```

Displays wallet server health and authentication status, including the wallet address.

## Example session

```bash theme={null}