# eth_sendRawTransaction: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_sendrawtransaction
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_sendRawTransaction", "params": ["0xf889808609184e72a00082271094000000000000000000000000000000000000000080a47f74657374320000000000000000000000000000000000000000000000000000006000571ca08a8bbf888cfa37bbf0bb965423625641fc956967b81d12e23709cead01446075a01ce999b56a8a88504be365442ea61239198e23d1fce7d00fcfc5cd3b44b7215f"]}'
```

### `eth_gasPrice`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}