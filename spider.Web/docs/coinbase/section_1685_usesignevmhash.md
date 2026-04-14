# useSignEvmHash
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignEvmHash



```ts theme={null}
function useSignEvmHash(): {
  signEvmHash: (options: SignEvmHashOptions) => Promise<SignEvmHashResult>;
};
```

Hook that provides a wrapped function to sign EVM messages with authentication checks.
This hook uses useEnforceAuthenticated to ensure the user is signed in before attempting to sign.

## Returns

```ts theme={null}
{
  signEvmHash: (options: SignEvmHashOptions) => Promise<SignEvmHashResult>;
}
```

| Name            | Type                                                                                                                                                                                                                                    |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signEvmHash()` | (`options`: [`SignEvmHashOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignEvmHashOptions)) => `Promise`\<[`SignEvmHashResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignEvmHashResult)> |

## Example

```tsx lines theme={null}
function SignHash() {
  const { signEvmHash } = useSignEvmHash();
  const { evmAddress } = useEvmAddress();

  const handleSign = async () => {
    if (!evmAddress) return;

    try {
      const result = await signEvmHash({
        evmAccount: evmAddress,
        hash: "0x3ea2f1d0abf3fc66cf29eebb70cbd4e7fe762ef8a09bcc06c8edf641230afec0"
      });
      console.log("Signature:", result.signature);
    } catch (error) {
      console.error("Failed to sign hash:", error);
    }
  };

  return (
    <button onClick={handleSign}>Sign Hash</button>
  );
}
```

