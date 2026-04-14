# UseKeyExportIframeResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/UseKeyExportIframeResult



Return type for the key export iframe hooks.

## Properties

| Property            | Type                                                 | Description                                                                                                                  |
| ------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| <a /> `status`      | `null` \| `SecureIframeStatus`                       | The current status of the iframe.                                                                                            |
| <a /> `message`     | `undefined` \| `string`                              | Optional message associated with the status.                                                                                 |
| <a /> `updateTheme` | (`theme`: `Partial`\<`SecureIframeTheme`>) => `void` | Function to update the theme of the iframe.                                                                                  |
| <a /> `cleanup`     | () => `void`                                         | Function to manually clean up the iframe. Note: Cleanup is automatic when the component unmounts or when the iframe expires. |

