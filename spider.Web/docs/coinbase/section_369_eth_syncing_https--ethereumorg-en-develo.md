# eth_syncing: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_syncing
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_syncing"}'
```

### `eth_feeHistory`

The [Billing Unit](/data/node/pricing) value of this method is 100.

```bash lines wrap theme={null}
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_feeHistory", "params": [4, "latest", [25, 75]]}'
```

### `eth_mining`

```bash lines wrap theme={null}