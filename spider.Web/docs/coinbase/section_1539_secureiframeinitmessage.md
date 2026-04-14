# SecureIframeInitMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeInitMessage



```ts theme={null}
type SecureIframeInitMessage = {
  type: SecureIframeEventType["INIT"];
  payload: SecureIframeContext;
};
```

The message sent to the secure iframe to initialize it.

## Properties

| Property        | Type                                                                                                                   |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- |
| <a /> `type`    | [`SecureIframeEventType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeEventType)\[`"INIT"`] |
| <a /> `payload` | [`SecureIframeContext`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeContext)                |

