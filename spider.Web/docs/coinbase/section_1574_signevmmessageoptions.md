# SignEvmMessageOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmMessageOptions



```ts theme={null}
type SignEvmMessageOptions = {
  evmAccount: EvmAddress;
  message: string;
  idempotencyKey?: string;
};
```

Request parameters for signing an EVM message.

## Properties

| Property                | Type                                                                                  | Description                                |
| ----------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| <a /> `evmAccount`      | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) | The EVM account to sign the message with.  |
| <a /> `message`         | `string`                                                                              | The message to sign.                       |
| <a /> `idempotencyKey?` | `string`                                                                              | Optional idempotency key for safe retries. |

