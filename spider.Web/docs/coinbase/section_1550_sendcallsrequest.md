# SendCallsRequest
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendCallsRequest



```ts theme={null}
type SendCallsRequest = {
  method: "wallet_sendCalls";
  params: [{
     calls: Call[];
     capabilities?: SendCallsCapabilities;
  }];
};
```

A request to send one or more calls to the specified Ethereum chain

## Properties

| Property       | Type                                                                                                                                                      |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `method` | `"wallet_sendCalls"`                                                                                                                                      |
| <a /> `params` | \[\{ `calls`: `Call`\[]; `capabilities?`: [`SendCallsCapabilities`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendCallsCapabilities); }] |

