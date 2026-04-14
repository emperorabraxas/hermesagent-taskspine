# getMessageFromUnknownError
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Utilities/getMessageFromUnknownError



```ts theme={null}
function getMessageFromUnknownError(error: unknown, defaultMesasge?: string): string;
```

Get a message from an unknown error with a fallback in case one is not found.

## Parameters

| Parameter         | Type      | Default value            | Description                                           |
| ----------------- | --------- | ------------------------ | ----------------------------------------------------- |
| `error`           | `unknown` | `undefined`              | The error to get a message from.                      |
| `defaultMesasge?` | `string`  | `"Something went wrong"` | The default message to return if no message is found. |

## Returns

`string`

The message from the error.

