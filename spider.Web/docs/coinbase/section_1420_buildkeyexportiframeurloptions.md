# BuildKeyExportIframeUrlOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/BuildKeyExportIframeUrlOptions



Options for building a key export iframe URL.

## Properties

| Property             | Type      | Description                                                                                |
| -------------------- | --------- | ------------------------------------------------------------------------------------------ |
| <a /> `projectId`    | `string`  | The project ID for authentication.                                                         |
| <a /> `basePath?`    | `string`  | The base path of the secure iframe. **Default** `"https://secure-wallet.cdp.coinbase.com"` |
| <a /> `label?`       | `string`  | The label for the button displayed in the iframe.                                          |
| <a /> `copiedLabel?` | `string`  | The label to display when the key is copied successfully.                                  |
| <a /> `icon?`        | `boolean` | Whether to show an icon in the button. **Default** `true`                                  |

