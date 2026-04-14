# useSwap
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSwap



```ts theme={null}
function useSwap(): UseSwapReturnType;
```

Hook that executes a token swap and waits for on-chain confirmation.

For EOA accounts, waits for a transaction receipt.
For smart accounts, polls the user operation until it completes.

## Returns

[`UseSwapReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseSwapReturnType)

UseSwapReturnType

## Example

```tsx theme={null}
import { useSwap } from "@coinbase/cdp-hooks";

function SwapComponent() {
  const { swap, data, status, error } = useSwap();

  const handleSwap = () => {
    swap({
      network: "base",
      fromToken: "0x4200000000000000000000000000000000000006",
      toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      fromAmount: "100000000000000000",
      slippageBps: 100,
    });
  };

  return (
    <div>
      <button onClick={handleSwap} disabled={status === "pending"}>
        {status === "pending" ? "Swapping..." : "Swap"}
      </button>
      {status === "success" && data && <p>Swap confirmed!</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}
```

