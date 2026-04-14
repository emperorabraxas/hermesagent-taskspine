# VerifyEmailOTPResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/VerifyEmailOTPResult



```ts theme={null}
type VerifyEmailOTPResult = {
  user: User;
  message: string;
  isNewUser: boolean;
};
```

Result of verifyEmailOTP.

## Properties

| Property          | Type                                                                       | Description                          |
| ----------------- | -------------------------------------------------------------------------- | ------------------------------------ |
| <a /> `user`      | [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/User) | The successfully logged-in user.     |
| <a /> `message`   | `string`                                                                   | The message to display to the user.  |
| <a /> `isNewUser` | `boolean`                                                                  | Whether the user is newly signed up. |

