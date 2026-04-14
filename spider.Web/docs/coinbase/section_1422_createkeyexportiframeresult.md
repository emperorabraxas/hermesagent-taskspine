# CreateKeyExportIframeResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/CreateKeyExportIframeResult



Result of setting up a key export iframe.

## Properties

| Property            | Type                                                                                                                                 | Description                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| <a /> `iframe`      | `HTMLIFrameElement`                                                                                                                  | The iframe element that was set up.                         |
| <a /> `cleanup`     | () => `void`                                                                                                                         | Function to clean up event listeners and remove the iframe. |
| <a /> `updateTheme` | (`theme`: `Partial`\<[`SecureIframeTheme`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeTheme)>) => `void` | Function to update the theme of the iframe.                 |

