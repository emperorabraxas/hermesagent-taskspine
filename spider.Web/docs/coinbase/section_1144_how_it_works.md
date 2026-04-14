# How It Works
Source: https://docs.cdp.coinbase.com/get-started/tools/cdp-cli-how-it-works

Credentials, environments, field syntax, and the encode-sign-send pipeline.

<Info>
  The CLI is self-documenting. Run `cdp --help` to see all commands, `cdp evm --help` to see actions in a group, or `cdp evm accounts create --help` to see fields, types, and examples for a specific action.
</Info>

## Auth and environments

The CLI uses two credentials, each serving a different purpose:

| Credential                    | What it does                                                                        | Where to get it                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **API key** (key ID + secret) | Authenticates all requests to the CDP API                                           | [Portal → API Keys](https://portal.cdp.coinbase.com/projects/api-keys)                    |
| **Wallet secret**             | Authorizes account operations: creating accounts, signing, and sending transactions | [Portal → Server Wallet](https://portal.cdp.coinbase.com/products/server-wallet/accounts) |

Both are stored in the OS keyring and used to generate short-lived JWTs for every request. Read-only operations like listing accounts or checking balances only need the API key. The wallet secret is additionally required whenever the request touches private key material.

### Environments

An environment is a named credential set. The built-in `live` environment has the CDP API URL pre-configured. Only keys need to be supplied.

```bash theme={null}
cdp env live --key-file ./cdp-api-key.json
cdp env live --wallet-secret-file ./cdp_wallet_secret.txt
cdp env                                    # list all environments
cdp env live --remove                      # remove an environment
cdp env live --remove-wallet-secret        # remove wallet secret (keeps API key)
```

**Multiple keys:** Prefix `live` with any name to create additional environments that inherit `live`'s URL:

```bash theme={null}
cdp env live-team-a --key-id <id> --key-secret <secret>
cdp evm accounts list -e live-team-a    # use for one request
```

Custom environment names that don't start with `live` require `--url`:

```bash theme={null}
cdp env custom --key-id <id> --key-secret <secret> --url https://api.cdp.coinbase.com/platform/v2
```

### Headless / environment variable configuration

As an alternative to `cdp env`, the CLI can be configured entirely through environment variables. This is useful when secrets are managed externally (Vault, AWS Secrets Manager, etc.) or in headless environments without an OS keyring:

| Variable            | Purpose                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| `CDP_ENV`           | Active environment name                                                 |
| `CDP_KEY_ID`        | API key ID                                                              |
| `CDP_KEY_SECRET`    | API key secret                                                          |
| `CDP_WALLET_SECRET` | Wallet secret                                                           |
| `CDP_URL`           | Base URL override                                                       |
| `CDP_NO_HISTORY`    | Set to `1` to disable request history                                   |
| `CDP_CONFIG_DIR`    | Config directory (default: `~/.config/cdp`, `%APPDATA%\cdp` on Windows) |

***

## Request workflow

Every resource action (`cdp <resource> <action>`) follows the same workflow. These flags work on any action:

### Discover

```bash theme={null}
cdp evm accounts create --help       # see fields, types, response shape, example
cdp evm accounts create --template   # print the full request body as JSON
```

### Compose

```bash theme={null}
cdp evm accounts create name=my-wallet                   # inline fields
cdp evm accounts create --edit                           # open in $EDITOR
cdp evm accounts create @body.json                       # from file
echo '{"name":"my-wallet"}' | cdp evm accounts create -  # from stdin
```

### Preview

```bash theme={null}
cdp evm accounts create --dry-run    # show the assembled request without sending
```

### Send and filter

```bash theme={null}
cdp evm accounts create name=my-wallet
cdp evm accounts list --jq '.accounts[].address'   # filter response with jq
cdp evm accounts list --paginate                   # auto-follow nextPageToken
```

### Reuse

The CLI saves the last successful request body per environment and action. On the next run, omit unchanged fields:

```bash theme={null}
cdp evm accounts create name=my-wallet   # saves on success
cdp evm accounts create                  # reuses saved values
cdp evm accounts create name=other       # overrides just the name
```

View or clear saved history with `cdp history`:

```bash theme={null}
cdp history        # show saved request history
cdp history clear  # clear all saved history
```

### Field syntax

| Syntax         | Meaning                                          |
| -------------- | ------------------------------------------------ |
| `key=value`    | String body field                                |
| `key:=value`   | Raw JSON body field (e.g. `'owners:=["0x..."]'`) |
| `key==value`   | Query parameter                                  |
| `a.b.c=value`  | Nested body field                                |
| `@file.json`   | Body from file                                   |
| `-`            | Body from stdin                                  |
| `Header:value` | Custom HTTP header                               |

***

## The encode-sign-send pipeline

Sending a transaction is a three-step process: **encode** an unsigned transaction locally, **sign** it with the account's private key in the [Trusted Execution Environment (TEE)](/server-wallets/v2/introduction/security), and **send** it to the network.

### EVM

```bash theme={null}
address=$(cdp evm accounts by-name my-wallet --jq '.address')
