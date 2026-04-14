# UseSwapReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseSwapReturnType



```ts theme={null}
type UseSwapReturnType = {
  swap: (options: ExecuteSwapOptions) => Promise<void>;
  data:   | SwapTransactionData
     | undefined;
  status: Status;
  error: Error | undefined;
  reset: () => void;
};
```

Return type of the `useSwap` hook.

## Properties

| Property       | Type                                                                                                                                      | Description                                                                       |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| <a /> `swap`   | (`options`: [`ExecuteSwapOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/ExecuteSwapOptions)) => `Promise`\<`void`> | The function to execute a swap.                                                   |
| <a /> `data`   | \| [`SwapTransactionData`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SwapTransactionData) \| `undefined`                | The data returned from the `swap` function.                                       |
| <a /> `status` | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                                            | The status of the `swap` function.                                                |
| <a /> `error`  | `Error` \| `undefined`                                                                                                                    | The error returned from the `swap` function or due to polling the user operation. |
| <a /> `reset`  | () => `void`                                                                                                                              | Resets the hook to its initial idle state, clearing data, error, and status.      |

