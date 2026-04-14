# useSignSolanaMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignSolanaMessage



```ts theme={null}
function useSignSolanaMessage(): {
  signSolanaMessage: (options: SignSolanaMessageOptions) => Promise<SignSolanaMessageResult>;
};
```

Hook that provides a wrapped function to sign messages with a Solana account with authentication checks.
This hook uses useEnforceAuthenticated to ensure the user is signed in before attempting to sign.

## Returns

```ts theme={null}
{
  signSolanaMessage: (options: SignSolanaMessageOptions) => Promise<SignSolanaMessageResult>;
}
```

| Name                  | Type                                                                             |
| --------------------- | -------------------------------------------------------------------------------- |
| `signSolanaMessage()` | (`options`: `SignSolanaMessageOptions`) => `Promise`\<`SignSolanaMessageResult`> |

## Example

```tsx lines theme={null}
function SignSolanaMessage() {
  const { signSolanaMessage } = useSignSolanaMessage();
  const { solanaAddress } = useSolanaAddress();

  const handleSign = async () => {
    if (!solanaAddress) return;

    try {
      const result = await signSolanaMessage({
        solanaAccount: solanaAddress,
        message: "Welcome to our dApp! Click to sign in."
      });
      console.log("Signature:", result.signature);
    } catch (error) {
      console.error("Failed to sign message:", error);
    }
  };

  return <button onClick={handleSign}>Sign Message</button>;
}
```

