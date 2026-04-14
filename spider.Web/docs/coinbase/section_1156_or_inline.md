# or inline
cdp env live --wallet-secret <secret>
```

<Tip>
  Run `cdp env` to verify. `live` should appear with the key ID and a `(wallet)` indicator.
</Tip>

## 3. Create an account

```bash theme={null}
cdp evm accounts create name=my-wallet
```

```json theme={null}
{
  "address": "0x3c0D84055994c3062819Ce8730869D0aDeA4c3Bf",
  "name": "my-wallet"
}
```

Server wallet accounts are network-agnostic. The same address works on any EVM network (Base, Ethereum, Arbitrum, etc.). The network is specified when sending a transaction.

## 4. Fund the account

Capture the address, then use the faucet to get testnet ETH:

```bash theme={null}
address=$(cdp evm accounts by-name my-wallet --jq '.address')
cdp evm faucet address=$address network=base-sepolia token=eth
```

Verify the funds arrived:

```bash theme={null}
cdp evm token-balances get base-sepolia $address
```

## 5. Send a transaction

This is the core workflow: **encode** an unsigned transaction, **sign** it with the account, and **send** it to the network.

```bash theme={null}