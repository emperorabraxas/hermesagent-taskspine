# ExportWalletCopyKeyButton
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletCopyKeyButton



```ts theme={null}
function ExportWalletCopyKeyButton(props: ExportWalletCopyKeyButtonProps): null | Element;
```

A button that copies the private key of an EVM or Solana account.

Note that an EVM smart account's private key cannot be exported. If a smart account address is provided, the button will not be rendered.

## Parameters

| Parameter | Type                                                                                                                           | Description                                            |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ |
| `props`   | [`ExportWalletCopyKeyButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ExportWalletCopyKeyButtonProps) | The props for the ExportWalletCopyKeyButton component. |

## Returns

`null` | `Element`

The rendered component.

## See

* [ExportWallet](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWallet)
* [CopyEvmKeyButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopyEvmKeyButton)
* [CopySolanaKeyButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopySolanaKeyButton)

## Example

```tsx lines theme={null}
// Render the ExportWalletCopyKeyButton component with custom labels
function ExportWalletCopyKeyButtonExample() {
  const { evmAddress } = useEvmAddress();
  if (!evmAddress) return null;
  return (
    <ExportWallet address={evmAddress}>
      <ExportWalletCopyKeyButton label="Copy private key" copiedLabel="Private key copied" />
    </ExportWallet>
  );
}
```

