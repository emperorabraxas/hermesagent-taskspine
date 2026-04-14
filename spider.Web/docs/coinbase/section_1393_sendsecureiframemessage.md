# sendSecureIframeMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/sendSecureIframeMessage



```ts theme={null}
function sendSecureIframeMessage(iframe: null | HTMLIFrameElement, message: SecureIframeKeyExportIncomingMessage): void;
```

Sends a message to the secure iframe.

## Parameters

| Parameter | Type                                                                                                                                      | Description                                |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `iframe`  | `null` \| `HTMLIFrameElement`                                                                                                             | The iframe element to send the message to. |
| `message` | [`SecureIframeKeyExportIncomingMessage`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeKeyExportIncomingMessage) | The message to send.                       |

## Returns

`void`

