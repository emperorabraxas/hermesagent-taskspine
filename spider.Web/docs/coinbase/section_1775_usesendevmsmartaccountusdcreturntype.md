# UseSendEvmSmartAccountUsdcReturnType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseSendEvmSmartAccountUsdcReturnType



```ts theme={null}
type UseSendEvmSmartAccountUsdcReturnType = {
  sendEvmSmartAccountUsdc: (options: SendEvmSmartAccountUsdcOptions) => Promise<SendEvmSmartAccountUsdcResult>;
} & UseWaitForUserOperationReturnType;
```

Represents the return type of the `useSendEvmSmartAccountUsdc` hook.
Extends UseWaitForUserOperationReturnType with a send function.

## Type declaration

| Name                        | Type                                                                                         |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| `sendEvmSmartAccountUsdc()` | (`options`: `SendEvmSmartAccountUsdcOptions`) => `Promise`\<`SendEvmSmartAccountUsdcResult`> |

