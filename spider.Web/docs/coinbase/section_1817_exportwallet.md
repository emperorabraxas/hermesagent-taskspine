# ExportWallet
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWallet



```ts theme={null}
function ExportWallet(props: ExportWalletProps): Element;
```

The ExportWallet component is used to export the private key of an EVM or Solana account.

Note that an EVM smart account's private key cannot be exported. If a smart account address is provided, a warning message will be displayed explaining that the private key cannot be copied, and the copy key button will not be rendered.

## Parameters

| Parameter | Type                                                                                               | Description                               |
| --------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| `props`   | [`ExportWalletProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ExportWalletProps) | The props for the ExportWallet component. |

## Returns

`Element`

The rendered component.

## See

* [ExportWalletTitle](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletTitle)
* [ExportWalletWarning](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletWarning)
* [ExportWalletCopyAddress](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletCopyAddress)
* [ExportWalletCopyKeyButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletCopyKeyButton)
* [ExportWalletFooter](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletFooter)

## Examples

```tsx lines theme={null}
// Render the ExportWallet component with an EVM address
function ExportWalletExample() {
  const { evmAddress } = useEvmAddress();
  return (
    <ExportWallet address={evmAddress} />
  );
}
```

```tsx lines theme={null}
// Render the ExportWallet component with a Solana address
function ExportWalletExample() {
  const { solanaAddress } = useSolanaAddress();
  return (
    <ExportWallet address={solanaAddress} />
  );
}
```

## Further reading

* [ExportWallet Overview](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWallet.README)

