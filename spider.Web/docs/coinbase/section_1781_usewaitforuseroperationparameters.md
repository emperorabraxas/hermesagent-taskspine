# UseWaitForUserOperationParameters
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseWaitForUserOperationParameters



```ts theme={null}
type UseWaitForUserOperationParameters = {
  userOperationHash?: Hex;
  evmSmartAccount?: EvmAddress;
  network?: SendEvmTransactionWithEndUserAccountBodyNetwork;
  enabled?: boolean;
};
```

Represents the parameters for the `useWaitForUserOperation` hook.

## Properties

| Property                   | Type                                                                                                                                                            |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `userOperationHash?` | [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Hex)                                                                                        |
| <a /> `evmSmartAccount?`   | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/EvmAddress)                                                                          |
| <a /> `network?`           | [`SendEvmTransactionWithEndUserAccountBodyNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmTransactionWithEndUserAccountBodyNetwork) |
| <a /> `enabled?`           | `boolean`                                                                                                                                                       |

