# debug_traceBlockByHash: https://geth.ethereum.org/docs/rpc/ns-debug#debug_traceblockbyhash
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "debug_traceBlockByHash", "params": ["0xe075488f2716495e97c43f6eb2994964074a70245cca5844b308479ccbbb9ae7", {"tracer": "callTracer"}]}'
```

### `debug_traceBlockByNumber`

The [Billing Unit](/data/node/pricing) value of this method is 500.

```bash lines wrap theme={null}