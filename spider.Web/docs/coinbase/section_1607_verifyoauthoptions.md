# VerifyOAuthOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyOAuthOptions



```ts theme={null}
type VerifyOAuthOptions = {
  flowId: string;
  code: string;
  providerType: OAuth2ProviderType;
  idempotencyKey?: string;
};
```

Request parameters for verifyOAuth.

## Properties

| Property                | Type                                                                                                  | Description                                |
| ----------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| <a /> `flowId`          | `string`                                                                                              | The flow ID to use in verifyOAuth.         |
| <a /> `code`            | `string`                                                                                              | The OAuth code to verify.                  |
| <a /> `providerType`    | [`OAuth2ProviderType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/OAuth2ProviderType) | The type of OAuth provider.                |
| <a /> `idempotencyKey?` | `string`                                                                                              | Optional idempotency key for safe retries. |

