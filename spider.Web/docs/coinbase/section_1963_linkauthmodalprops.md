# LinkAuthModalProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthModalProps



Props for the LinkAuthModal component.

## See

[LinkAuthModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthModal)

## Properties

| Property               | Type                                                                                                                      | Description                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| <a /> `children?`      | `ReactNode`                                                                                                               | If provided, will render the children instead of the default trigger button.               |
| <a /> `open?`          | `boolean`                                                                                                                 | Whether the modal is open. Note: if you set this, you must also set `setIsOpen`.           |
| <a /> `setIsOpen?`     | (`value`: `boolean`) => `void`                                                                                            | A function to set the modal's open state. Note: if you set this, you must also set `open`. |
| <a /> `onLinkSuccess?` | (`method`: \| `null` \| [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)) => `void` | A function to call when an auth method is successfully linked.                             |

