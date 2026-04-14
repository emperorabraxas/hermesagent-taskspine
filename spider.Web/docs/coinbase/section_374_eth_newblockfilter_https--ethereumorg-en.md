# eth_newBlockFilter: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_newblockfilter
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_newBlockFilter"}'
```

### `eth_uninstallFilter`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}