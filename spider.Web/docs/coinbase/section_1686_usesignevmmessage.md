# useSignEvmMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignEvmMessage



```ts theme={null}
function useSignEvmMessage(): {
  signEvmMessage: (options: SignEvmMessageOptions) => Promise<SignEvmMessageResult>;
};
```

Hook that provides a wrapped function to sign EVM messages with authentication checks.
This hook uses useEnforceAuthenticated to ensure the user is signed in before attempting to sign.

## Returns

```ts theme={null}
{
  signEvmMessage: (options: SignEvmMessageOptions) => Promise<SignEvmMessageResult>;
}
```

| Name               | Type                                                                                                                                                                                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signEvmMessage()` | (`options`: [`SignEvmMessageOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignEvmMessageOptions)) => `Promise`\<[`SignEvmMessageResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignEvmMessageResult)> |

## Example

```tsx lines theme={null}
function SignMessage() {
  const { signEvmMessage } = useSignEvmMessage();
  const { evmAddress } = useEvmAddress();

  const handleSign = async () => {
    if (!evmAddress) return;

    try {
      const result = await signEvmMessage({
        evmAccount: evmAddress,
        message: "Welcome to our dApp! Click to sign in."
      });
      console.log("Signature:", result.signature);
    } catch (error) {
      console.error("Failed to sign message:", error);
    }
  };

  return (
    <button onClick={handleSign}>Sign Message</button>
  );
}
```

