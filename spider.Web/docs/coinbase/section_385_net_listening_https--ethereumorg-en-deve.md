# net_listening: https://ethereum.org/en/developers/docs/apis/json-rpc/#net_listening
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "net_listening"}'
```

### `net_peercount`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}