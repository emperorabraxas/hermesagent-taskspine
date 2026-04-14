# InitiateSmsMfaResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/InitiateSmsMfaResult



```ts theme={null}
type InitiateSmsMfaResult = {
  method: "sms";
  success: boolean;
};
```

Result of SMS MFA enrollment initiation.

## Properties

| Property        | Type      | Description                          |
| --------------- | --------- | ------------------------------------ |
| <a /> `method`  | `"sms"`   | The MFA method that was initiated.   |
| <a /> `success` | `boolean` | Indicates SMS was sent successfully. |

