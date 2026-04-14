# Send (Solana send does not take an address; it is inferred from the transaction)
cdp solana accounts send transaction \
  network=solana-devnet \
  transaction=$SIGNED
```

### Smart accounts

Smart accounts ([ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)) use user operations instead of the encode-sign-send pipeline:

```bash theme={null}
cdp evm smart-accounts user-operations prepare-and-send 0xSmartAddr \
  network=base-sepolia \
  'calls:=[{"to":"0xRecipient","value":"10000000000000","data":"0x"}]' \
  paymasterUrl=https://paymaster.cdp.coinbase.com
```

***

## `cdp api`

Browse the embedded API spec or make raw authenticated requests:

```bash theme={null}
cdp api                          # list all API groups
cdp api /evm                     # list all endpoints in a group
cdp api /evm/accounts --help     # full detail for endpoint(s) at that path
cdp api /evm/accounts            # GET request
cdp api -X POST /evm/accounts name=my-wallet   # POST request
cdp api /evm/accounts -v         # verbose (show headers)
```

Same field syntax as resource commands, plus `Header:value` for custom HTTP headers.

***

## Client-side utilities

`cdp util` commands run locally. See `cdp util <command> -h` for full options.

| Command       | What it does                                                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tx-encode`   | Build an unsigned EVM or Solana transaction. Auto-fetches nonce/gas/blockhash when `--from` is provided. Supports `--value 0.001ether` and `--value 0.5sol` unit syntax. |
| `tx-decode`   | Decode a raw transaction (hex for EVM, base64 for Solana) to inspect its contents.                                                                                       |
| `abi-encode`  | ABI-encode function calls (`"transfer(address,uint256)" 0x... 1000`) or raw value tuples.                                                                                |
| `encrypt-key` | Encrypt a private key for account import using CDP's RSA public key. Accepts `--file` or stdin.                                                                          |

***

## Agent skills

Bundled skills teach AI agents complete workflows. Install them with `cdp skills add`.

```bash theme={null}
cdp skills list                # list installed skills
cdp skills add                 # install/update all bundled skills
cdp skills add --dir <path>    # install to a specific directory
cdp skills remove              # remove all installed skills
```

Skills cover: account creation and funding, the encode-sign-send pipeline, signing, import/export, smart accounts, spend permissions, token swaps, data queries, policies, end users, onramp, Solana, and x402.

