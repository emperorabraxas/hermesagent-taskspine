# eth_getTransactionReceipt: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_gettransactionreceipt
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionReceipt", "params": ["0x633982a26e0cfba940613c52b31c664fe977e05171e35f62da2426596007e249"]}'
```

### `eth_getTransactionByBlockHashAndIndex`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}