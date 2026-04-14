# SecureIframeStatusMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeStatusMessage



```ts theme={null}
type SecureIframeStatusMessage = {
  type: SecureIframeEventType["STATUS"];
  payload: {
     status: SecureIframeStatus;
     message?: string;
  };
};
```

The message sent from the secure iframe to the parent window to indicate the status of the private key retrieval.

## Properties

| Property           | Type                                                                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `type`       | [`SecureIframeEventType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeEventType)\[`"STATUS"`]                    |
| <a /> `payload`    | \{ `status`: [`SecureIframeStatus`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeStatus); `message?`: `string`; } |
| `payload.status`   | [`SecureIframeStatus`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeStatus)                                       |
| `payload.message?` | `string`                                                                                                                                    |

