# useGetSwapPrice
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useGetSwapPrice



```ts theme={null}
function useGetSwapPrice(options: UseGetSwapPriceOptions): UseGetSwapPriceReturnType;
```

Reactive query hook that fetches a non-binding indicative price for a token swap.
Automatically fetches when the user is signed in and all required parameters are provided.
Includes preflight `issues` in the response (e.g. insufficient balance or allowance).

When the token pair, network, account, or userId changes, previous data is cleared. When only the
amount or slippage changes, previous data is preserved while the new price loads
(stale-while-revalidate).

## Parameters

| Parameter | Type                                                                                                         | Description                             |
| --------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| `options` | [`UseGetSwapPriceOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/UseGetSwapPriceOptions) | Configuration for the swap price query. |

## Returns

[`UseGetSwapPriceReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseGetSwapPriceReturnType)

An object containing the swap price data, status, error, refetch, and reset functions.

## Example

```tsx theme={null}
import { useGetSwapPrice } from "@coinbase/cdp-hooks";

function SwapPriceDisplay() {
  const [fromAmount, setFromAmount] = useState("");

  const { data, status, error, refetch, reset } = useGetSwapPrice({
    network: "base",
    fromToken: "0x4200000000000000000000000000000000000006",
    toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    fromAmount,
  });

  return (
    <div>
      <input
        value={fromAmount}
        onChange={(e) => setFromAmount(e.target.value)}
        placeholder="0"
      />
      {status === "pending" && <p>Loading price...</p>}
      {data?.liquidityAvailable && <p>Expected output: {data.toAmount}</p>}
      {error && <p>Error: {error.message}</p>}
      <button onClick={refetch} disabled={status === "pending"}>Refresh</button>
      <button onClick={reset}>Clear</button>
    </div>
  );
}
```

