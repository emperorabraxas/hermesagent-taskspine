# VerifyTelegramOAuthOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyTelegramOAuthOptions



```ts theme={null}
type VerifyTelegramOAuthOptions = {
  flowId: string;
  telegramData: TelegramAuthData;
};
```

Request parameters for verifyTelegramOAuth.

## Properties

| Property             | Type                                                                                            | Description                                     |
| -------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| <a /> `flowId`       | `string`                                                                                        | The flow ID from initiateAuthentication.        |
| <a /> `telegramData` | [`TelegramAuthData`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/TelegramAuthData) | The Telegram auth data received from the popup. |

