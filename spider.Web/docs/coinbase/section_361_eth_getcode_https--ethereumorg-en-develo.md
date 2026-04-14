# eth_getCode: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_getcode
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getCode", "params":["0x7f268357a8c2552623316e2562d90e642bb538e5", "latest"]}'
```

### `eth_getTransactionCount`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}