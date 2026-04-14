# useSignSolanaTransaction
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignSolanaTransaction



```ts theme={null}
function useSignSolanaTransaction(): {
  signSolanaTransaction: (options: SignSolanaTransactionOptions) => Promise<SignSolanaTransactionResult>;
};
```

Hook that provides a wrapped function to sign Solana transactions with authentication checks.
This hook uses useEnforceAuthenticated to ensure the user is signed in before attempting to sign.

## Returns

```ts theme={null}
{
  signSolanaTransaction: (options: SignSolanaTransactionOptions) => Promise<SignSolanaTransactionResult>;
}
```

| Name                      | Type                                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| `signSolanaTransaction()` | (`options`: `SignSolanaTransactionOptions`) => `Promise`\<`SignSolanaTransactionResult`> |

## Example

```tsx lines theme={null}
function SignSolanaTransaction() {
  const { signSolanaTransaction } = useSignSolanaTransaction();
  const { solanaAddress } = useSolanaAddress();

  const handleSign = async () => {
    if (!solanaAddress) return;

    try {
      const result = await signSolanaTransaction({
        solanaAccount: solanaAddress,
        transaction: "base64-encoded-transaction"
      });
      console.log("Signed Transaction:", result.signedTransaction);
    } catch (error) {
      console.error("Failed to sign transaction:", error);
    }
  };

  return (
    <button onClick={handleSign}>Sign Solana Transaction</button>
  );
}
```

