# SwapFees
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwapFees



```ts theme={null}
type SwapFees = {
  gasFee?:   | TokenFee
     | null;
  protocolFee?:   | TokenFee
     | null;
};
```

The estimated fees for the swap.

## Properties

| Property             | Type                                                                                         | Description                              |
| -------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------- |
| <a /> `gasFee?`      | \| [`TokenFee`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/TokenFee) \| `null` | The estimated gas fee for the swap.      |
| <a /> `protocolFee?` | \| [`TokenFee`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/TokenFee) \| `null` | The estimated protocol fee for the swap. |

