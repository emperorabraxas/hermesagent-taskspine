# net_peercount: https://ethereum.org/en/developers/docs/apis/json-rpc/#net_peercount
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "net_peerCount"}'
```

## Web3 Namespace

Below are example requests for JSON-RPC API methods in the `web3_*` namespace.

### `web3_clientVersion`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}