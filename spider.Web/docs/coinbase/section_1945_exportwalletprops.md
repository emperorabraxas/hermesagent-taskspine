# ExportWalletProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ExportWalletProps



The props for the ExportWallet component.

## See

[ExportWallet](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWallet)

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLDivElement`>, `"children"`>

## Properties

| Property                        | Type                                                                                                                                | Description                                                                                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `children?`               | \| `ReactNode` \| (`props`: \{ `type`: `"solana"` \| `"evm-eoa"` \| `"evm-smart"`; `isSessionExpired`: `boolean`; }) => `ReactNode` | The children to render. If a function is provided, it will be called with the address type and isSessionExpired as props.                             |
| <a /> `address`                 | `string`                                                                                                                            | The address of the account to export.                                                                                                                 |
| <a /> `onIframeReady?`          | () => `void`                                                                                                                        | A function to call when the iframe UI is ready.                                                                                                       |
| <a /> `onCopySuccess?`          | () => `void`                                                                                                                        | A function to call when the key is copied successfully.                                                                                               |
| <a /> `onIframeError?`          | (`error?`: `string`) => `void`                                                                                                      | A function to call when there is an error in the secure iframe                                                                                        |
| <a /> `onIframeSessionExpired?` | () => `void`                                                                                                                        | A function to call when the iframe session has expired.                                                                                               |
| <a /> `skipMfa?`                | `boolean`                                                                                                                           | Skip the MFA verification flow. Set to true if you want to handle MFA verification separately or if you're using your own MFA UI. **Default** `false` |

