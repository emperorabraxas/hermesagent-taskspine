# eth_submitHashrate: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_submithashrate
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_submitHashrate", "params":["0x500000", "0x59daa26581d0acd1fce254fb7e85952f4c09d0915afd33d3886cd914bc7d283c"]}'
```

## Debug Namespace

Below are example requests for JSON-RPC API method in the `debug_*` namespace.

<Info>
  For API methods in the `debug_*` namespace, we only support the following tracer types: `callTracer`.
</Info>

### `debug_traceBlockByHash`

The [Billing Unit](/data/node/pricing) value of this method is 500.

```bash lines wrap theme={null}