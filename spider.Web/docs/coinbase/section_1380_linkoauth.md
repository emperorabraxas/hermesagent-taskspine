# linkOAuth
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/linkOAuth



```ts theme={null}
function linkOAuth(providerType: OAuth2ProviderType, options?: {
  idempotencyKey?: string;
}): Promise<void>;
```

Links an OAuth account to the current user.

## Parameters

| Parameter                 | Type                                                                                                  | Description                                                         |
| ------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `providerType`            | [`OAuth2ProviderType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/OAuth2ProviderType) | The OAuth provider type (e.g., "google", "apple", "x", "telegram"). |
| `options?`                | \{ `idempotencyKey?`: `string`; }                                                                     | Optional options for the link operation.                            |
| `options.idempotencyKey?` | `string`                                                                                              | Optional idempotency key for safe retries.                          |

## Returns

`Promise`\<`void`>

The result of the link OAuth initiation.

