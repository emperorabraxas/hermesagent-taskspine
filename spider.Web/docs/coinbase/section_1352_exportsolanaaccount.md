# exportSolanaAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/exportSolanaAccount



```ts theme={null}
function exportSolanaAccount(options: ExportSolanaAccountOptions): Promise<ExportSolanaAccountResult>;
```

Exports the private key of a Solana account.

## Parameters

| Parameter | Type                                                                                                                  | Description                            |
| --------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `options` | [`ExportSolanaAccountOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportSolanaAccountOptions) | The options for exporting the account. |

## Returns

`Promise`\<[`ExportSolanaAccountResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportSolanaAccountResult)>

The result of the export.

## Example

```typescript lines theme={null}
const result = await exportSolanaAccount({
  solanaAccount: "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
});
```

## Deprecated

This function will be removed soon. Use `createSolanaKeyExportIframe` instead for a more secure key export experience
that never exposes the private key to your application's JavaScript context.

## See

[createSolanaKeyExportIframe](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/createSolanaKeyExportIframe)

