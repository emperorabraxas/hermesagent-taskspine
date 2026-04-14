# eth_uninstallFilter: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_uninstallfilter
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_uninstallFilter", "params":["0x81440f9af726125cb7fc671eb0f2d8728d6ad699989a"]}'
```

### `eth_getFilterChanges`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}