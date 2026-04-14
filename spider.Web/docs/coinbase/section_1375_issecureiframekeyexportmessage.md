# isSecureIframeKeyExportMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/isSecureIframeKeyExportMessage



```ts theme={null}
function isSecureIframeKeyExportMessage(message: unknown): message is SecureIframeOutgoingMessage | SecureIframeKeyExportIncomingMessage;
```

Checks if the message is a key export message.

## Parameters

| Parameter | Type      | Description           |
| --------- | --------- | --------------------- |
| `message` | `unknown` | The message to check. |

## Returns

message is SecureIframeOutgoingMessage | SecureIframeKeyExportIncomingMessage

True if the message is a key export message, false otherwise.

