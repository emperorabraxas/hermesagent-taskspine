# SendEvmEoaUsdcOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmEoaUsdcOptions



```ts theme={null}
type SendEvmEoaUsdcOptions = {
  evmAccount: EvmAddress;
  to: EvmAddress;
  amount: string;
  network: SendEvmUsdcNetwork;
  idempotencyKey?: string;
};
```

Request parameters for sending EVM USDC from an EOA account.

## Properties

| Property                | Type                                                                                                  | Description                                                                      |
| ----------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| <a /> `evmAccount`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                 | The EVM EOA account to send USDC from.                                           |
| <a /> `to`              | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                 | The recipient address.                                                           |
| <a /> `amount`          | `string`                                                                                              | The amount of USDC to send in human-readable format (e.g., "1.50" for 1.5 USDC). |
| <a /> `network`         | [`SendEvmUsdcNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmUsdcNetwork) | The network to send USDC on.                                                     |
| <a /> `idempotencyKey?` | `string`                                                                                              | Optional idempotency key for safe retries.                                       |

