# signInWithEmail
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/signInWithEmail



```ts theme={null}
function signInWithEmail(options: SignInWithEmailOptions): Promise<SignInWithEmailResult>;
```

Initiates the sign in flow with an email.

## Parameters

| Parameter | Type                                                                                                          | Description                  |
| --------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `options` | [`SignInWithEmailOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignInWithEmailOptions) | The options for the sign in. |

## Returns

`Promise`\<[`SignInWithEmailResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignInWithEmailResult)>

The result of the sign in.

## Example

```typescript lines theme={null}
const result = await signInWithEmail({
  email: "user@example.com"
});
```

