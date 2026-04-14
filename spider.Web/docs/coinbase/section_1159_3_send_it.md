# 3. Send it
cdp evm accounts send transaction $address \
  network=base-sepolia \
  transaction=$SIGNED
```

A `transactionHash` appears in the response. Verify the balance changed:

```bash theme={null}
cdp evm token-balances get base-sepolia $address
```

Your first on-chain transaction is complete.

<Info>
  The encode-sign-send pipeline is covered in detail on the [How it works](/get-started/tools/cdp-cli-how-it-works) page, including ERC-20 transfers, Solana, and smart accounts.
</Info>

## Troubleshooting

| Error                                  | Cause                              | Fix                                                                                     |
| -------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------- |
| `Must use a CDP Entity scoped API key` | Using a legacy key                 | Create a new API key in the [Portal](https://portal.cdp.coinbase.com/projects/api-keys) |
| `Wallet authentication error`          | Wallet secret missing or incorrect | Re-add with `cdp env live --wallet-secret-file`                                         |
| `forbidden`                            | API key permissions issue          | Check key permissions in the Portal                                                     |
| `cdp: command not found`               | CLI not on PATH                    | Run `npm install -g @coinbase/cdp-cli` again; on Windows, add `%APPDATA%\npm` to PATH   |

