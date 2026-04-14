# SendEvmSmartAccountUsdcOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmSmartAccountUsdcOptions



```ts theme={null}
type SendEvmSmartAccountUsdcOptions = {
  evmSmartAccount: EvmAddress;
  to: EvmAddress;
  amount: string;
  network: SendEvmUsdcNetwork;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
};
```

Request parameters for sending EVM USDC from a Smart Account.

## Properties

| Property                 | Type                                                                                                  | Description                                                                      |
| ------------------------ | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| <a /> `evmSmartAccount`  | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                 | The EVM Smart Account to send USDC from.                                         |
| <a /> `to`               | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                 | The recipient address.                                                           |
| <a /> `amount`           | `string`                                                                                              | The amount of USDC to send in human-readable format (e.g., "1.50" for 1.5 USDC). |
| <a /> `network`          | [`SendEvmUsdcNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmUsdcNetwork) | The network to send USDC on.                                                     |
| <a /> `useCdpPaymaster?` | `boolean`                                                                                             | Whether to use CDP Paymaster to sponsor gas fees.                                |
| <a /> `paymasterUrl?`    | `string`                                                                                              | Optional custom Paymaster URL to use for gas sponsorship.                        |
| <a /> `idempotencyKey?`  | `string`                                                                                              | Optional idempotency key for safe retries.                                       |

