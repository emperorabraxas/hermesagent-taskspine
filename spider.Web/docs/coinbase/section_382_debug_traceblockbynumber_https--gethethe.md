# debug_traceBlockByNumber: https://geth.ethereum.org/docs/rpc/ns-debug#debug_traceblockbynumber
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "debug_traceBlockByNumber", "params": ["0xe11130", {"tracer": "callTracer"}]}'
```

### `debug_traceCall`

The [Billing Unit](/data/node/pricing) value of this method is 500.

```bash lines wrap theme={null}