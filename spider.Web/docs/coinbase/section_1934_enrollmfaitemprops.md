# EnrollMfaItemProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaItemProps



The props for the EnrollMfaItem component.

## See

[EnrollMfaItem](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaItem)

## Properties

| Property           | Type                                      | Description                                                   |
| ------------------ | ----------------------------------------- | ------------------------------------------------------------- |
| <a /> `method`     | `"totp"` \| `"sms"`                       | The MFA method this item represents                           |
| <a /> `icon?`      | `ReactNode`                               | An icon to display                                            |
| <a /> `label`      | `string`                                  | A label for the MFA method                                    |
| <a /> `isPending?` | `boolean`                                 | Whether this method's enrollment is pending                   |
| <a /> `onSetUp`    | `MouseEventHandler`\<`HTMLButtonElement`> | A function to call when the user clicks to set up this method |

