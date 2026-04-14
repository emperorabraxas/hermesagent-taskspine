# fetchWithX402
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/fetchWithX402



```ts theme={null}
function fetchWithX402(options: FetchWithX402Options): FetchWithX402ReturnType;
```

Hook that provides a wrapped fetch function with payment handling.

## Parameters

| Parameter | Type                                                                                                      | Description                                 |
| --------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `options` | [`FetchWithX402Options`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/FetchWithX402Options) | Configuration object for the fetch function |

## Returns

[`FetchWithX402ReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/FetchWithX402ReturnType)

A wrapped fetch function with payment handling

## Example

```tsx lines theme={null}
const { fetchWithPayment } = fetchWithX402();
const response = await fetchWithPayment("https://x402-resource.com", {
  method: "GET",
});
```

