# SignInWithSmsOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignInWithSmsOptions



```ts theme={null}
type SignInWithSmsOptions = {
  phoneNumber: string;
  idempotencyKey?: string;
};
```

Request parameters for signInWithSms.

## Properties

| Property                | Type     | Description                                                               |
| ----------------------- | -------- | ------------------------------------------------------------------------- |
| <a /> `phoneNumber`     | `string` | The phone number of the end user in E.164 format. Example: "+14155552671" |
| <a /> `idempotencyKey?` | `string` | Optional idempotency key for safe retries.                                |

