# CopyAddressProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/CopyAddressProps



The props for the CopyAddress component.

## See

[CopyAddress](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopyAddress)

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLDivElement`>, `"children"`>

## Properties

| Property               | Type         | Description                                                 | Overrides     |
| ---------------------- | ------------ | ----------------------------------------------------------- | ------------- |
| <a /> `address`        | `string`     | The address to copy.                                        | -             |
| <a /> `label?`         | `string`     | The label for the input.                                    | -             |
| <a /> `onCopy?`        | () => `void` | A function to call when the address copy button is clicked. | `Omit.onCopy` |
| <a /> `onCopySuccess?` | () => `void` | A function to call when the address is copied successfully. | -             |

