# isApiError
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Utilities/isApiError



```ts theme={null}
function isApiError(error: unknown): error is APIError;
```

Type guard to check if the error is an API error.

## Parameters

| Parameter | Type      | Description         |
| --------- | --------- | ------------------- |
| `error`   | `unknown` | The error to check. |

## Returns

`error is APIError`

* True if the error is an API error, false otherwise.

## Example

```tsx lines theme={null}
try {
  ...
}
catch (error) {
  if (isApiError(error)) {
    // Handle API error
    console.log(error.errorMessage);
  }
}
```

