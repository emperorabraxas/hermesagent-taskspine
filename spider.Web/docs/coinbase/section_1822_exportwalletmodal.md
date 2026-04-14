# ExportWalletModal
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletModal



```ts theme={null}
function ExportWalletModal(props: ExportWalletModalProps): Element;
```

A export wallet modal component that wraps the [ExportWallet](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWallet) component.

## Parameters

| Parameter | Type                                                                                                         | Description                                    |
| --------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| `props`   | [`ExportWalletModalProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ExportWalletModalProps) | The props for the ExportWalletModal component. |

## Returns

`Element`

The ExportWalletModal component.

## See

* [ExportWalletModalClose](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletModalClose) for the modal close button.
* [ExportWalletModalContent](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletModalContent) for the modal content.
* [ExportWalletModalTitle](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletModalTitle) for the modal title.
* [ExportWalletModalTrigger](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletModalTrigger) for the trigger button.

## Examples

```tsx lines theme={null}
// Render the ExportWalletModal component with an EVM address
function ExportWalletModalExample() {
  const { evmAddress } = useEvmAddress();
  return (
    <ExportWalletModal address={evmAddress} />
  );
}
```

```tsx lines theme={null}
// Render the ExportWalletModal component with a Solana address
function ExportWalletModalExample() {
  const { solanaAddress } = useSolanaAddress();
  return (
    <ExportWalletModal address={solanaAddress} />
  );
}
```

```tsx lines theme={null}
// Render the ExportWalletModal component with a custom label for the trigger button
function ExportWalletModalExample() {
  const { solanaAddress } = useSolanaAddress();
  return (
    <ExportWalletModal address={solanaAddress}>
      <ExportWalletModalTrigger label="Export Solana wallet" />
    </ExportWalletModal>
  );
}
```

```tsx lines theme={null}
// Render the ExportWalletModal component with a custom button as the trigger
function ExportWalletModalExample() {
  const { solanaAddress } = useSolanaAddress();
  return (
    <ExportWalletModal address={solanaAddress}>
      <button type="button">Export Solana wallet</button>
    </ExportWalletModal>
  );
}
```

```tsx lines theme={null}
// Render the ExportWalletModal component with customized content
function ExportWalletModalExample() {
  const { solanaAddress } = useSolanaAddress();
  return (
    <ExportWalletModal address={solanaAddress}>
      <ExportWalletModalTrigger />
      <ExportWalletModalContent>
        <ExportWallet address={solanaAddress}>
          <div className="header">
            <ExportWalletModalTitle />
            <ExportWalletModalClose />
          </div>
          <div className="content">
            <ExportWalletWarning />
            <ExportWalletCopyAddress />
            <ExportWalletCopyKeyButton />
            <p className="help-text">
              Your private key gives full control of your wallet.
              Store it safely and never share it with anyone.
            </p>
          </div>
        </ExportWallet>
      </ExportWalletModalContent>
    </ExportWalletModal>
  );
}
```

