# EvmCall
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmCall



```ts theme={null}
type EvmCall = {
  to: EvmAddress;
  value?: bigint;
  data?: Hex;
};
```

Represents a call in an EVM user operation.

## Properties

| Property       | Type                                                                                  | Description                               |
| -------------- | ------------------------------------------------------------------------------------- | ----------------------------------------- |
| <a /> `to`     | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | The target address for the call.          |
| <a /> `value?` | `bigint`                                                                              | The value to send with the call (in wei). |
| <a /> `data?`  | [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Hex)               | The data to send with the call.           |

