# net_version: https://ethereum.org/en/developers/docs/apis/json-rpc#net_version
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "net_version"}'
```

### `net_listening`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}