# useSendSolanaUsdc
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSendSolanaUsdc



```ts theme={null}
function useSendSolanaUsdc(): {
  sendSolanaUsdc: (options: SendSolanaUsdcOptions) => Promise<SendSolanaUsdcResult>;
};
```

Hook to send USDC on the Solana network.

## Returns

```ts theme={null}
{
  sendSolanaUsdc: (options: SendSolanaUsdcOptions) => Promise<SendSolanaUsdcResult>;
}
```

| Name               | Type                                                                       |
| ------------------ | -------------------------------------------------------------------------- |
| `sendSolanaUsdc()` | (`options`: `SendSolanaUsdcOptions`) => `Promise`\<`SendSolanaUsdcResult`> |

## Example

```tsx theme={null}
import { useSendSolanaUsdc, useSolanaAddress } from "@coinbase/cdp-hooks";

function MyComponent() {
  const { sendSolanaUsdc } = useSendSolanaUsdc();
  const { solanaAddress } = useSolanaAddress();

  const handleSendUsdc = async () => {
    if (!solanaAddress) return;

    try {
      const result = await sendSolanaUsdc({
        solanaAccount: solanaAddress,
        to: "ExXhNkgYf6efh7YyqDRVxPZuzafobao1A74drUdp8trd",
        amount: "10.00",
        network: "solana-devnet",
        createRecipientAta: true,
      });
      console.log("Transaction Signature:", result.transactionSignature);
    } catch (error) {
      console.error("Failed to send USDC:", error);
    }
  };

  return <button onClick={handleSendUsdc}>Send USDC on Solana</button>;
}
```

