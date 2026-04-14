# verifyTelegramOAuth
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/verifyTelegramOAuth



```ts theme={null}
function verifyTelegramOAuth(options: VerifyTelegramOAuthOptions): Promise<VerifyOAuthResult>;
```

Verifies a Telegram OAuth authentication by calling the verifyOAuthEndUserIdentity endpoint.

## Parameters

| Parameter | Type                                                                                                                  | Description                                                              |
| --------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `options` | [`VerifyTelegramOAuthOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyTelegramOAuthOptions) | The options containing the flowId and Telegram auth data from the popup. |

## Returns

`Promise`\<[`VerifyOAuthResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyOAuthResult)>

The result of the verification.

