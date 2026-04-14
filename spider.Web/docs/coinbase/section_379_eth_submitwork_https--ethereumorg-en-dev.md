# eth_submitWork: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_submitwork
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_submitWork", "params": ["0x0000000000000001", "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef", "0xD1FE5700000000000000000000000000D1FE5700000000000000000000000000"]}'
```

### `eth_submitHashrate`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}