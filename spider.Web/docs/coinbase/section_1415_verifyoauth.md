# verifyOAuth
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/verifyOAuth



```ts theme={null}
function verifyOAuth(options: VerifyOAuthOptions): Promise<VerifyOAuthResult>;
```

Verifies the OAuth code for the sign in flow with a OAuth provider.

## Parameters

| Parameter | Type                                                                                                  | Description                       |
| --------- | ----------------------------------------------------------------------------------------------------- | --------------------------------- |
| `options` | [`VerifyOAuthOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyOAuthOptions) | The options for the verification. |

## Returns

`Promise`\<[`VerifyOAuthResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyOAuthResult)>

The result of the verification.

## Examples

```typescript lines theme={null}
// Google
const result = await verifyOAuth({
  flowId: "flow-id-from-signInWithGoogle",
  code: "123456", // The OAuth code received from the OAuth provider
  providerType: "google",
});
```

```typescript lines theme={null}
// Apple
const result = await verifyOAuth({
  flowId: "flow-id-from-signInWithApple",
  code: "123456", // The OAuth code received from the OAuth provider
  providerType: "apple",
});
```

```typescript lines theme={null}
// X
const result = await verifyOAuth({
  flowId: "flow-id-from-signInWithX",
  code: "123456", // The OAuth code received from the OAuth provider
  providerType: "x",
});
```

