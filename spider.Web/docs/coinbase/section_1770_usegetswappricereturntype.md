# UseGetSwapPriceReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseGetSwapPriceReturnType



```ts theme={null}
type UseGetSwapPriceReturnType = {
  data:   | GetSwapPriceResult
     | SwapUnavailableResult
     | undefined;
  status: Status;
  error: Error | undefined;
  refetch: () => void;
  reset: () => void;
};
```

Return type of the `useGetSwapPrice` hook.

## Properties

| Property        | Type                                                                                                                                                                                                                                     | Description                                                                                                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a /> `data`    | \| [`GetSwapPriceResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/GetSwapPriceResult) \| [`SwapUnavailableResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SwapUnavailableResult) \| `undefined` | The most recent result from `getSwapPrice`. Cleared when the token pair, network, account, or userId changes. Preserved as stale data during re-fetches triggered by amount or slippage changes. |
| <a /> `status`  | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                                                                                                                                           | The status of the `getSwapPrice` function.                                                                                                                                                       |
| <a /> `error`   | `Error` \| `undefined`                                                                                                                                                                                                                   | The error returned from the `getSwapPrice` function.                                                                                                                                             |
| <a /> `refetch` | () => `void`                                                                                                                                                                                                                             | A function to refetch the swap price.                                                                                                                                                            |
| <a /> `reset`   | () => `void`                                                                                                                                                                                                                             | A function to reset the state of the hook.                                                                                                                                                       |

