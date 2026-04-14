# eth_getLogs: https://ethereum.org/en/developers/docs/apis/json-rpc#eth_getlogs
curl -s {Your_Endpoint_URL} -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "id": 1, "method": "eth_getLogs", "params": [{"fromBlock": "0xdad3c1", "toBlock": "0xdad3c2"}]}'
```

<Info>
  `eth_getLogs` has a max block range limit of `1000` blocks.
</Info>

### `eth_call`

The [Billing Unit](/data/node/pricing) value of this method is 30.

```bash lines wrap theme={null}