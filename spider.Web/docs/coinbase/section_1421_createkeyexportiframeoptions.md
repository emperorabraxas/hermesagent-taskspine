# CreateKeyExportIframeOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/CreateKeyExportIframeOptions



Options for setting up a key export iframe.

## Properties

| Property                | Type                                                                                                                                              | Description                                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `address`         | `string`                                                                                                                                          | The address of the account to export.                                                                                                         |
| <a /> `target`          | `string` \| `HTMLElement`                                                                                                                         | The target element: either a CSS selector string or an HTMLElement container. An iframe will be created and appended to the target container. |
| <a /> `projectId`       | `string`                                                                                                                                          | The project ID for authentication.                                                                                                            |
| <a /> `label?`          | `string`                                                                                                                                          | The label for the button displayed in the iframe.                                                                                             |
| <a /> `copiedLabel?`    | `string`                                                                                                                                          | The label to display when the key is copied successfully.                                                                                     |
| <a /> `icon?`           | `boolean`                                                                                                                                         | Whether to show an icon in the button. **Default** `true`                                                                                     |
| <a /> `theme?`          | `Partial`\<[`SecureIframeTheme`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeTheme)>                                   | Theme overrides for the iframe button.                                                                                                        |
| <a /> `onStatusUpdate?` | (`status`: [`SecureIframeStatus`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeStatus), `message?`: `string`) => `void` | Callback invoked when the iframe status changes.                                                                                              |

