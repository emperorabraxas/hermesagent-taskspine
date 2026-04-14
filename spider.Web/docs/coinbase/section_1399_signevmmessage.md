# signEvmMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/signEvmMessage



```ts theme={null}
function signEvmMessage(options: SignEvmMessageOptions): Promise<SignEvmHashResult>;
```

Signs an EVM message.

## Parameters

| Parameter | Type                                                                                                        | Description                  |
| --------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `options` | [`SignEvmMessageOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmMessageOptions) | The options for the signing. |

## Returns

`Promise`\<[`SignEvmHashResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmHashResult)>

The result of the signing.

## Example

```typescript lines theme={null}
const user = await getCurrentUser();
const evmAccount = user?.evmAccountObjects[0]?.address;

const result = await signEvmMessage({
  evmAccount,
  message: "Hello World" // Message to sign
});

```

