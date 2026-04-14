# sendIframeMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Utilities/sendIframeMessage



```ts theme={null}
function sendIframeMessage<T>(el: null | HTMLIFrameElement, message: T): void;
```

Sends a message to an iframe.

## Type Parameters

| Type Parameter                                                       |
| -------------------------------------------------------------------- |
| `T` *extends* `Record`\<`string` \| `number` \| `symbol`, `unknown`> |

## Parameters

| Parameter | Type                          | Description                                |
| --------- | ----------------------------- | ------------------------------------------ |
| `el`      | `null` \| `HTMLIFrameElement` | The iframe element to send the message to. |
| `message` | `T`                           | The message to send to the iframe.         |

## Returns

`void`

