# useExportSolanaAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useExportSolanaAccount



```ts theme={null}
function useExportSolanaAccount(): {
  exportSolanaAccount: (options: ExportSolanaAccountOptions) => Promise<ExportSolanaAccountResult>;
};
```

Hook that provides a wrapped function to export Solana account private keys with authentication checks.
This hook uses useEnforceAuthenticated to ensure the user is signed in before attempting to export.

## Returns

```ts theme={null}
{
  exportSolanaAccount: (options: ExportSolanaAccountOptions) => Promise<ExportSolanaAccountResult>;
}
```

| Name                    | Type                                                                                                                                                                                                                                                                    |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exportSolanaAccount()` | (`options`: [`ExportSolanaAccountOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/ExportSolanaAccountOptions)) => `Promise`\<[`ExportSolanaAccountResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/ExportSolanaAccountResult)> |

## Example

```tsx lines theme={null}
function ExportSolanaPrivateKey() {
  const { exportSolanaAccount } = useExportSolanaAccount();
  const { solanaAddress } = useSolanaAddress();

  const handleExport = async () => {
    if (!solanaAddress) return;

    try {
      const { privateKey } = await exportSolanaAccount({
        solanaAccount: solanaAddress
      });
      console.log("Private Key:", privateKey);
    } catch (error) {
      console.error("Failed to export private key:", error);
    }
  };

  return (
    <button onClick={handleExport}>Export Private Key</button>
  );
}
```

## Deprecated

This function will be removed soon. Use `useSolanaKeyExportIframe` instead for a more secure key export experience
that never exposes the private key to your application's JavaScript context.

## See

[useSolanaKeyExportIframe](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSolanaKeyExportIframe)

