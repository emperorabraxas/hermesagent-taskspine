# useEvmAddress
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useEvmAddress



```ts theme={null}
function useEvmAddress(): {
  evmAddress: null | `0x${string}`;
};
```

Hook to access the user's primary EVM (Ethereum Virtual Machine) address.
Returns the first Smart Account if available, otherwise returns the first EOA.
If the user has neither, this will return null.

**Note:** This hook always returns the first account (index 0) as the "primary" address.
If your users may have multiple accounts and need to select between them, use
`useEvmAccounts()` instead to get all accounts with metadata.

**Priority:** Smart Account \[0] → EOA \[0] → null

## Returns

```ts theme={null}
{
  evmAddress: null | `0x${string}`;
}
```

| Name         | Type                          |
| ------------ | ----------------------------- |
| `evmAddress` | `null` \| `` `0x${string}` `` |

## Example

```tsx lines theme={null}
function EVMWalletInfo() {
  const { evmAddress } = useEvmAddress();

  if (!evmAddress) {
    return <p>No EVM wallet connected</p>;
  }

  return (
    <div>
      <h3>Your EVM Wallet</h3>
      <p>Address: {evmAddress}</p>
    </div>
  );
}
```

## See

* useEvmAccounts for multi-account support
* useEvmSmartAccounts for smart account specific access

