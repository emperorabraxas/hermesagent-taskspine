# eth_getTransactionCount: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_gettransactioncount
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionCount", "params":["0xe222489ae12e15713cc1d65dd0ab2f5b18721bfd", "latest"]}'
```

### `eth_chainId`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}