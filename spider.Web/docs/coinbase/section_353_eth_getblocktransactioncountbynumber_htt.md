# eth_getBlockTransactionCountByNumber: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_getblocktransactioncountbynumber
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getBlockTransactionCountByNumber", "params": ["0xdad3c1"]}'
```

### `eth_getTransactionByHash`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}