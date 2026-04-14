# signInWithOAuth
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/signInWithOAuth



```ts theme={null}
function signInWithOAuth(providerType: OAuth2ProviderType, options?: {
  idempotencyKey?: string;
}): Promise<void>;
```

Initiates the sign in flow with an OAuth provider (Google, Apple, Telegram, and X are currently supported).
In a web application, this will redirect the user to the OAuth provider's sign in page.
This sign in method is not yet supported on mobile.

## Parameters

| Parameter                 | Type                                                                                                  | Description                                 |
| ------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `providerType`            | [`OAuth2ProviderType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/OAuth2ProviderType) | The type of OAuth provider to sign in with. |
| `options?`                | \{ `idempotencyKey?`: `string`; }                                                                     | Optional options for the sign in.           |
| `options.idempotencyKey?` | `string`                                                                                              | Optional idempotency key for safe retries.  |

## Returns

`Promise`\<`void`>

The result of the sign in.

## Examples

```typescript lines theme={null}
// Google
try {
 void signInWithOAuth("google");
} catch (error) {
  console.error("Failed to sign in with Google:", error);
}
```

```typescript lines theme={null}
// Apple
try {
 void signInWithOAuth("apple");
} catch (error) {
 console.error("Failed to sign in with Apple:", error);
}
```

```typescript lines theme={null}
// X
try {
 void signInWithOAuth("x");
} catch (error) {
 console.error("Failed to sign in with X:", error);
}
```

