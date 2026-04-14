# useSendEvmEoaUsdc
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSendEvmEoaUsdc



```ts theme={null}
function useSendEvmEoaUsdc(): {
  sendEvmEoaUsdc: (options: SendEvmEoaUsdcOptions) => Promise<SendEvmEoaUsdcResult>;
  data: TransactionState;
};
```

Hook to send USDC on an EVM network from an EOA (Externally Owned Account).

This hook waits for the transaction receipt and provides real-time status updates.

## Returns

```ts theme={null}
{
  sendEvmEoaUsdc: (options: SendEvmEoaUsdcOptions) => Promise<SendEvmEoaUsdcResult>;
  data: TransactionState;
}
```

| Name               | Type                                                                                               |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| `sendEvmEoaUsdc()` | (`options`: `SendEvmEoaUsdcOptions`) => `Promise`\<`SendEvmEoaUsdcResult`>                         |
| `data`             | [`TransactionState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/TransactionState) |

## Example

```tsx theme={null}
import { useSendEvmEoaUsdc, useEvmAddress } from "@coinbase/cdp-hooks";

function MyComponent() {
  const { sendEvmEoaUsdc, data } = useSendEvmEoaUsdc();
  const { evmAddress } = useEvmAddress();

  const handleSendUsdc = async () => {
    if (!evmAddress || data.status === "pending") return;

    try {
      const result = await sendEvmEoaUsdc({
        evmAccount: evmAddress,
        to: "0x1234567890123456789012345678901234567890",
        amount: "25.50",
        network: "base-sepolia",
      });

      console.log("Transaction Hash:", result.transactionHash);
    } catch (error) {
      console.error("Failed to send USDC:", error);
    }
  };

  const isPending = data.status === "pending";

  return (
    <div>
      <button aria-disabled={isPending} onClick={handleSendUsdc}>
        {isPending ? "Sending USDC..." : "Send USDC"}
      </button>
      {data.status === "success" && <p>USDC sent successfully</p>}
      {data.status === "error" && <p>Error: {data.error?.message ?? "Unable to send USDC"}</p>}
    </div>
  );
}
```

