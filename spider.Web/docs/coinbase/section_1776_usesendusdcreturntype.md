# UseSendUsdcReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseSendUsdcReturnType



```ts theme={null}
type UseSendUsdcReturnType = {
  sendUsdc: (options: SendUsdcOptions) => Promise<SendUsdcResult>;
  data:   | SendUsdcTransactionData
     | undefined;
  error: Error | undefined;
  status: Status;
};
```

Represents the return type of the `useSendUsdc` hook.

## Properties

| Property         | Type                                                                                                                               |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `sendUsdc` | (`options`: `SendUsdcOptions`) => `Promise`\<`SendUsdcResult`>                                                                     |
| <a /> `data`     | \| [`SendUsdcTransactionData`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SendUsdcTransactionData) \| `undefined` |
| <a /> `error`    | `Error` \| `undefined`                                                                                                             |
| <a /> `status`   | [`Status`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status)                                                     |

