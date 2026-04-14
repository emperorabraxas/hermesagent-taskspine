# CopyEvmKeyButtonProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/CopyEvmKeyButtonProps



The props for the CopyEvmKeyButton component.

## See

* [CopyEvmKeyButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopyEvmKeyButton)
* [IframeTheme](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/IframeTheme)

## Extends

* `Pick`\<[`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps), `"size"` | `"fullWidth"`>

## Properties

| Property                  | Type                                                                                   | Description                                                    | Inherited from   |
| ------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ---------------- |
| <a /> `address`           | `string`                                                                               | The address of the evm account to copy.                        | -                |
| <a /> `className?`        | `string`                                                                               | The class name to apply to the button.                         | -                |
| <a /> `copiedLabel?`      | `string`                                                                               | The label to display when the private key is copied.           | -                |
| <a /> `icon?`             | `boolean`                                                                              | Whether to show an icon in the button.                         | -                |
| <a /> `label?`            | `string`                                                                               | The label to display on the button.                            | -                |
| <a /> `onReady?`          | () => `void`                                                                           | A function to call when the iframe UI is ready.                | -                |
| <a /> `onSessionExpired?` | () => `void`                                                                           | A function to call when the iframe session has expired.        | -                |
| <a /> `onSuccess?`        | () => `void`                                                                           | A function to call when the key is copied successfully.        | -                |
| <a /> `onError?`          | (`error?`: `string`) => `void`                                                         | A function to call when there is an error in the secure iframe | -                |
| <a /> `theme?`            | `Partial`\<`SecureIframeTheme`>                                                        | Theme overrides for the iframe.                                | -                |
| <a /> `variant?`          | `"primary"` \| `"secondary"`                                                           | The variant of the button.                                     | -                |
| <a /> `size?`             | [`ButtonSize`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonSize) | The size of the button. Defaults to "md".                      | `Pick.size`      |
| <a /> `fullWidth?`        | `boolean`                                                                              | Whether the button should be full width.                       | `Pick.fullWidth` |

