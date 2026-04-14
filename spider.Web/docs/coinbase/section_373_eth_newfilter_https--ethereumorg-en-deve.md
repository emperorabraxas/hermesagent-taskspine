# eth_newFilter: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_newfilter
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_newFilter", "params":[{}]}'
```

### `eth_newBlockFilter`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}