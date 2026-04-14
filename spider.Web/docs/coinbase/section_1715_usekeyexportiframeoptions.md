# UseKeyExportIframeOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/UseKeyExportIframeOptions



Options for the EVM and Solana key export iframe hooks.

## Properties

| Property             | Type                                  | Description                                                       |
| -------------------- | ------------------------------------- | ----------------------------------------------------------------- |
| <a /> `address`      | `string`                              | The address of the account to export.                             |
| <a /> `containerRef` | `RefObject`\<`null` \| `HTMLElement`> | A ref to the container element where the iframe will be appended. |
| <a /> `label?`       | `string`                              | The label for the button displayed in the iframe.                 |
| <a /> `copiedLabel?` | `string`                              | The label to display when the key is copied successfully.         |
| <a /> `icon?`        | `boolean`                             | Whether to show an icon in the button. **Default** `true`         |
| <a /> `theme?`       | `Partial`\<`SecureIframeTheme`>       | Theme overrides for the iframe button.                            |

