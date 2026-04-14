# getSecureIframeOrigin
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getSecureIframeOrigin



```ts theme={null}
function getSecureIframeOrigin(url: string): string;
```

Extracts the origin from a URL string.

## Parameters

| Parameter | Type     | Description                         |
| --------- | -------- | ----------------------------------- |
| `url`     | `string` | The URL to extract the origin from. |

## Returns

`string`

The origin string, or empty string if parsing fails.

