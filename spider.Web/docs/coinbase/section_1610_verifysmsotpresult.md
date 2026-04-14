# VerifySmsOTPResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifySmsOTPResult



```ts theme={null}
type VerifySmsOTPResult = {
  user: User;
  message: string;
  isNewUser: boolean;
};
```

Result of verifySmsOTP.

## Properties

| Property          | Type                                                                      | Description                          |
| ----------------- | ------------------------------------------------------------------------- | ------------------------------------ |
| <a /> `user`      | [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/User) | The successfully logged-in user.     |
| <a /> `message`   | `string`                                                                  | The message to display to the user.  |
| <a /> `isNewUser` | `boolean`                                                                 | Whether the user is newly signed up. |

