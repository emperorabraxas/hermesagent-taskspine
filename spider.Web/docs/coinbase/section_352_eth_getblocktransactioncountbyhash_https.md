# eth_getBlockTransactionCountByHash: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_getblocktransactioncountbyhash
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getBlockTransactionCountByHash", "params": ["0x849a3ac8f0d81df1a645701cdb9f90e58500d2eabb80ff3b7f4e8c13f025eff2"]}'
```

### `eth_getBlockTransactionCountByNumber`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}