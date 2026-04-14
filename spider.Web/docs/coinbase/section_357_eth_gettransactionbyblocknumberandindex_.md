# eth_getTransactionByBlockNumberAndIndex: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_gettransactionbyblocknumberandindex
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionByBlockNumberAndIndex", "params": ["0xdad3c1", "0x0"]}'
```

### `eth_getLogs`

The [Billing Unit](/data/node/pricing) value of this method is 100.

```bash lines wrap theme={null}