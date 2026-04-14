# debug_traceCall: https://geth.ethereum.org/docs/rpc/ns-debug#debug_traceCall
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"debug_traceCall","params":[{"from":"0x000000000000000000000000000000000000dead","to":"0x111111111111111111111111111111111111dead","gas":"0x30D40","gasPrice":"0x3B9ACA00","value":"0x0","data":"0xa9059cbb000000000000000000000000222222222222222222222222222222222222dead00000000000000000000000000000000000000000000000000000000000000ff"},"latest",{"tracer":"callTracer"}]}'
```

## Net Namespace

Below are example requests for JSON-RPC API method in the `net_*` namespace.

### `net_version`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}