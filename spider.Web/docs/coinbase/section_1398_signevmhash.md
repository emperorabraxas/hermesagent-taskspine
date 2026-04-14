# signEvmHash
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/signEvmHash



```ts theme={null}
function signEvmHash(options: SignEvmHashOptions): Promise<SignEvmHashResult>;
```

Signs a hash with an EVM account.

## Parameters

| Parameter | Type                                                                                                  | Description                  |
| --------- | ----------------------------------------------------------------------------------------------------- | ---------------------------- |
| `options` | [`SignEvmHashOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmHashOptions) | The options for the signing. |

## Returns

`Promise`\<[`SignEvmHashResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmHashResult)>

The result of the signing.

## Example

```typescript lines theme={null}
const result = await signEvmHash({
  evmAccount: "0x1234...",
  hash: "0xabcd..." // 32-byte hex string to sign
});
```

