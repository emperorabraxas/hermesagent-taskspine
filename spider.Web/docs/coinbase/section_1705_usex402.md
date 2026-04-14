# useX402
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useX402



```ts theme={null}
function useX402(options: FetchWithX402Options): FetchWithX402ReturnType;
```

Hook that provides a fetch function with X402 payment handling.

## Parameters

| Parameter | Type                   | Description                                 |
| --------- | ---------------------- | ------------------------------------------- |
| `options` | `FetchWithX402Options` | Configuration object for the fetch function |

## Returns

`FetchWithX402ReturnType`

A fetch function with X402 payment handling

## Example

```tsx lines theme={null}
const { fetchWithPayment } = useX402();
const response = await fetchWithPayment("https://x402-resource.com", {
  method: "GET",
});
```

