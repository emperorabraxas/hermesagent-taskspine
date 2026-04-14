# SmsAuthentication
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SmsAuthentication



```ts theme={null}
type SmsAuthentication = {
  type: "sms";
  phoneNumber: string;
};
```

The SMS authentication method.

## Properties

| Property            | Type     | Description                                       |
| ------------------- | -------- | ------------------------------------------------- |
| <a /> `type`        | `"sms"`  | The type of authentication method.                |
| <a /> `phoneNumber` | `string` | The phone number of the end user in E.164 format. |

