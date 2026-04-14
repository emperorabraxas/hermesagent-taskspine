# eth_call: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_call
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params":[{ "to": "0x514910771af9ca656af840dff83e8264ecf986ca", "data": "0x70a08231000000000000000000000000f27eee60abacb983251fea941dd7350280a538ba"}, "latest"]}'
```

### `eth_getBalance`

```bash lines wrap theme={null}