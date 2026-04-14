# eth_getBalance: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_getbalance
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getBalance", "params":["0x8d97689c9818892b700e27f316cc3e41e17fbeb9", "latest"]}'
```

### `eth_getCode`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}