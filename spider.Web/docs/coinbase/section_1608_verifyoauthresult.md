# VerifyOAuthResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/VerifyOAuthResult



```ts theme={null}
type VerifyOAuthResult = {
  user: User;
  message: string;
  isNewUser: boolean;
};
```

Result of verifyOAuth.

## Properties

| Property          | Type                                                                      | Description                          |
| ----------------- | ------------------------------------------------------------------------- | ------------------------------------ |
| <a /> `user`      | [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/User) | The successfully logged-in user.     |
| <a /> `message`   | `string`                                                                  | The message to display to the user.  |
| <a /> `isNewUser` | `boolean`                                                                 | Whether the user is newly signed up. |

