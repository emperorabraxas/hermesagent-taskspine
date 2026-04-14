# LinkAuthItemProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthItemProps



The props for the LinkAuthItem component.

## See

[LinkAuthItem](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthItem)

## Properties

| Property           | Type                                                                                   | Description                                                                 |
| ------------------ | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| <a /> `authMethod` | [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod) | A user-readable label for the auth method                                   |
| <a /> `isLinked`   | `boolean`                                                                              | Whether the auth method is linked to the current user's account             |
| <a /> `isPending?` | `boolean`                                                                              | Whether the auth method linking is pending                                  |
| <a /> `icon?`      | `ReactNode`                                                                            | An icon to display                                                          |
| <a /> `label`      | `string`                                                                               | A label for the auth method                                                 |
| <a /> `userAlias?` | `string`                                                                               | The user alias for the auth method (i.e. email address, phone number, etc.) |
| <a /> `onLink`     | `MouseEventHandler`\<`HTMLButtonElement`>                                              | A function to call when the auth method is linked.                          |

