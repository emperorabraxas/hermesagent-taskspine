# AuthenticationMethods
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/AuthenticationMethods



```ts theme={null}
type AuthenticationMethods = {
  email?: EmailAuthentication;
  sms?: SmsAuthentication;
  google?: OAuth2Authentication;
  apple?: OAuth2Authentication;
  x?: OAuth2Authentication & {
     username?: string;
  };
  telegram?: TelegramAuthentication;
};
```

The authentication methods used by the user.

## Properties

| Property          | Type                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------- |
| <a /> `email?`    | [`EmailAuthentication`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EmailAuthentication) |
| <a /> `sms?`      | [`SmsAuthentication`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SmsAuthentication)     |
| <a /> `google?`   | `OAuth2Authentication`                                                                                  |
| <a /> `apple?`    | `OAuth2Authentication`                                                                                  |
| <a /> `x?`        | `OAuth2Authentication` & \{ `username?`: `string`; }                                                    |
| <a /> `telegram?` | `TelegramAuthentication`                                                                                |

