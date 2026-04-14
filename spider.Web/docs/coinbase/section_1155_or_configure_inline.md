# Or configure inline
cdp env live --key-id <id> --key-secret <secret>
```

Verify it works:

```bash theme={null}
cdp evm accounts list
```

An empty project returns `{"accounts":[]}`. This is expected.

## 2. Add a wallet secret

The [wallet secret](/server-wallets/v2/introduction/security#wallet-secrets) is a separate credential required for any operation that touches private keys (creating accounts, signing, sending).

Generate one in the [Server Wallet](https://portal.cdp.coinbase.com/products/server-wallet/accounts) section of the Portal. Look for **Generate Wallet Secret**, then download the file.

```bash theme={null}
cdp env live --wallet-secret-file ./cdp_wallet_secret.txt