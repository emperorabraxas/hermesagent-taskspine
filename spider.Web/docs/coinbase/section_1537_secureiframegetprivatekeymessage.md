# SecureIframeGetPrivateKeyMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeGetPrivateKeyMessage



```ts theme={null}
type SecureIframeGetPrivateKeyMessage = {
  type: SecureIframeKeyExportEventType["GET_PRIVATE_KEY"];
  payload: SecureIframeContext & {
     address: string;
     type: SecureIframeChainType;
  };
};
```

The message sent to the secure iframe to trigger fetching the private key.

## Properties

| Property        | Type                                                                                                                                                                                                                                                     |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `type`    | [`SecureIframeKeyExportEventType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeKeyExportEventType)\[`"GET_PRIVATE_KEY"`]                                                                                                      |
| <a /> `payload` | [`SecureIframeContext`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeContext) & \{ `address`: `string`; `type`: [`SecureIframeChainType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeChainType); } |

