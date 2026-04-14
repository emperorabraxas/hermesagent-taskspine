# FundFormProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundFormProps



The props for the FundForm component.

## Extends

* `Omit`\<`FormHTMLAttributes`\<`HTMLFormElement`>, `"children"`>

## Properties

| Property                             | Type                                                                                                             |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| <a /> `children?`                    | (`params`: \{ `view`: `"form"` \| `"error"` \| `"transaction-status"`; `Content`: `ReactNode`; }) => `ReactNode` |
| <a /> `openIn?`                      | `"popup"` \| `"tab"`                                                                                             |
| <a /> `submitLabel?`                 | `ReactNode`                                                                                                      |
| <a /> `onPopupOpen?`                 | (`popup`: `Window`) => `void`                                                                                    |
| <a /> `onPopupClose?`                | () => `void`                                                                                                     |
| <a /> `unmountOnTransactionError?`   | `boolean`                                                                                                        |
| <a /> `unmountOnTransactionSuccess?` | `boolean`                                                                                                        |
| <a /> `unmount?`                     | () => `void`                                                                                                     |

