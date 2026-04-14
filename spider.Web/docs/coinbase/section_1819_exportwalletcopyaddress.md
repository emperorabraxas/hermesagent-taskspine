# ExportWalletCopyAddress
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletCopyAddress



```ts theme={null}
function ExportWalletCopyAddress(props: ExportWalletCopyAddressProps): Element;
```

Displays a truncated address with a copy button.

## Parameters

| Parameter | Type                                                                                                                       | Description                                          |
| --------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `props`   | [`ExportWalletCopyAddressProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ExportWalletCopyAddressProps) | The props for the ExportWalletCopyAddress component. |

## Returns

`Element`

The rendered component.

## See

* [ExportWallet](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWallet)
* [CopyAddress](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopyAddress)

## Example

```tsx lines theme={null}
// Render the ExportWalletCopyAddress component with a custom label
function ExportWalletCopyKeyButtonExample() {
  const { evmAddress } = useEvmAddress();
  if (!evmAddress) return null;
  return (
    <ExportWallet address={evmAddress}>
      <ExportWalletCopyAddress label="My wallet address" />
    </ExportWallet>
  );
}
```

