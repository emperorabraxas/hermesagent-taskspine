# useSolanaStandardWallets
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-solana-standard-wallet/Functions/useSolanaStandardWallets



```ts theme={null}
function useSolanaStandardWallets(): {
  wallets: readonly Wallet[];
};
```

Hook to get all Standard Solana Wallets registered in the wallet standard.

This hook:

* Gets all wallets using getWallets().get()
* Listens for wallet registration/unregistration events
* Returns the complete list including the CDP wallet once registered

## Returns

```ts theme={null}
{
  wallets: readonly Wallet[];
}
```

Object containing array of all registered wallets

| Name      | Type                 |
| --------- | -------------------- |
| `wallets` | readonly `Wallet`\[] |

## Example

```tsx theme={null}
function WalletList() {
  const { wallets } = useSolanaStandardWallets();

  return (
    <div>
      <h3>Available Wallets:</h3>
      {wallets.map((wallet) => (
        <div key={wallet.name}>
          {wallet.name} {wallet.features['cdp:'] ? '(CDP)' : ''}
        </div>
      ))}
    </div>
  );
}
```

