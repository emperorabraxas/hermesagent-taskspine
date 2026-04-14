# eth_estimateGas: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_estimategas
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_estimateGas", "params": [{"from": "0x8d97689c9818892b700e27f316cc3e41e17fbeb9", "to": "0xd3cda913deb6f67967b99d67acdfa1712c293601", "value": "0x1"}]}'
```

### `eth_protocolVersion`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}