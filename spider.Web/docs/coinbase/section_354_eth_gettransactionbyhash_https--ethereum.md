# eth_getTransactionByHash: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_gettransactionbyhash
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionByHash", "params": ["0x633982a26e0cfba940613c52b31c664fe977e05171e35f62da2426596007e249"]}'
```

### `eth_getTransactionReceipt`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}