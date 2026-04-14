# SendCallsCapabilities
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendCallsCapabilities



```ts theme={null}
type SendCallsCapabilities = {
[key: string]: unknown;
  paymasterService?: {
     url?: string;
  };
  dataSuffix?: {
     value: Hex;
  };
};
```

Capabilities for wallet\_sendCalls

## Indexable

```ts theme={null}
[key: string]: unknown
```

## Properties

| Property                  | Type                                                                                   |
| ------------------------- | -------------------------------------------------------------------------------------- |
| <a /> `paymasterService?` | \{ `url?`: `string`; }                                                                 |
| `paymasterService.url?`   | `string`                                                                               |
| <a /> `dataSuffix?`       | \{ `value`: [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Hex); } |
| `dataSuffix.value`        | [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Hex)                |

