# SignInWithSmsResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignInWithSmsResult



```ts theme={null}
type SignInWithSmsResult = {
  message: string;
  flowId: string;
};
```

Result of signInWithSms.

## Properties

| Property        | Type     | Description                         |
| --------------- | -------- | ----------------------------------- |
| <a /> `message` | `string` | The message to display to the user. |
| <a /> `flowId`  | `string` | The flow ID to use in verifySmsOTP. |

