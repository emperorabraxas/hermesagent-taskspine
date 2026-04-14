# STANDARD_ERROR_CODES
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Variables/STANDARD_ERROR_CODES



```ts theme={null}
const STANDARD_ERROR_CODES: {
  rpc: {
     invalidInput: -32000;
     resourceNotFound: -32001;
     resourceUnavailable: -32002;
     transactionRejected: -32003;
     methodNotSupported: -32004;
     limitExceeded: -32005;
     parse: -32700;
     invalidRequest: -32600;
     methodNotFound: -32601;
     invalidParams: -32602;
     internal: -32603;
  };
  provider: {
     userRejectedRequest: 4001;
     unauthorized: 4100;
     unsupportedMethod: 4200;
     disconnected: 4900;
     chainDisconnected: 4901;
     unsupportedChain: 4902;
  };
};
```

Standard error codes for EIP1193 providers and JSON-RPC methods

## Type declaration

| Name                           | Type                                                                                                                                                                                                                                                                                                                  |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `rpc`                    | \{ `invalidInput`: `-32000`; `resourceNotFound`: `-32001`; `resourceUnavailable`: `-32002`; `transactionRejected`: `-32003`; `methodNotSupported`: `-32004`; `limitExceeded`: `-32005`; `parse`: `-32700`; `invalidRequest`: `-32600`; `methodNotFound`: `-32601`; `invalidParams`: `-32602`; `internal`: `-32603`; } |
| `rpc.invalidInput`             | `-32000`                                                                                                                                                                                                                                                                                                              |
| `rpc.resourceNotFound`         | `-32001`                                                                                                                                                                                                                                                                                                              |
| `rpc.resourceUnavailable`      | `-32002`                                                                                                                                                                                                                                                                                                              |
| `rpc.transactionRejected`      | `-32003`                                                                                                                                                                                                                                                                                                              |
| `rpc.methodNotSupported`       | `-32004`                                                                                                                                                                                                                                                                                                              |
| `rpc.limitExceeded`            | `-32005`                                                                                                                                                                                                                                                                                                              |
| `rpc.parse`                    | `-32700`                                                                                                                                                                                                                                                                                                              |
| `rpc.invalidRequest`           | `-32600`                                                                                                                                                                                                                                                                                                              |
| `rpc.methodNotFound`           | `-32601`                                                                                                                                                                                                                                                                                                              |
| `rpc.invalidParams`            | `-32602`                                                                                                                                                                                                                                                                                                              |
| `rpc.internal`                 | `-32603`                                                                                                                                                                                                                                                                                                              |
| <a /> `provider`               | \{ `userRejectedRequest`: `4001`; `unauthorized`: `4100`; `unsupportedMethod`: `4200`; `disconnected`: `4900`; `chainDisconnected`: `4901`; `unsupportedChain`: `4902`; }                                                                                                                                             |
| `provider.userRejectedRequest` | `4001`                                                                                                                                                                                                                                                                                                                |
| `provider.unauthorized`        | `4100`                                                                                                                                                                                                                                                                                                                |
| `provider.unsupportedMethod`   | `4200`                                                                                                                                                                                                                                                                                                                |
| `provider.disconnected`        | `4900`                                                                                                                                                                                                                                                                                                                |
| `provider.chainDisconnected`   | `4901`                                                                                                                                                                                                                                                                                                                |
| `provider.unsupportedChain`    | `4902`                                                                                                                                                                                                                                                                                                                |

