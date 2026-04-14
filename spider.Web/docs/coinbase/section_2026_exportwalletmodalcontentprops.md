# ExportWalletModalContentProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ExportWalletModalContentProps



```ts theme={null}
type ExportWalletModalContentProps = Omit<ModalContentProps, "children"> & Pick<ExportWalletProps, "children"> & {
  title?: ReactNode;
};
```

Props for the export wallet modal content.

## Type declaration

| Name     | Type        | Description                    |
| -------- | ----------- | ------------------------------ |
| `title?` | `ReactNode` | A title for the dialog element |

## See

[ExportWalletModalContent](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletModalContent)

