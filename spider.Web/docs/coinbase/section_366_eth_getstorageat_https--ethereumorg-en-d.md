# eth_getStorageAt: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_getstorageat
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getStorageAt", "params": ["0x6c8f2a135f6ed072de4503bd7c4999a1a17f824b", "0x0", "latest"]}'
```

### `eth_estimateGas`

The [Billing Unit](/data/node/pricing) value of this method is 100.

```bash lines wrap theme={null}