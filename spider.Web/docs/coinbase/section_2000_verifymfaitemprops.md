# VerifyMfaItemProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaItemProps



The props for the VerifyMfaItem component.

## See

[VerifyMfaItem](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaItem)

## Properties

| Property         | Type                                      | Description                                           |
| ---------------- | ----------------------------------------- | ----------------------------------------------------- |
| <a /> `method`   | `"totp"` \| `"sms"`                       | The MFA method this item represents.                  |
| <a /> `icon?`    | `ReactNode`                               | An icon to display.                                   |
| <a /> `label`    | `string`                                  | A label for the MFA method.                           |
| <a /> `onSelect` | `MouseEventHandler`\<`HTMLButtonElement`> | A function to call when the user selects this method. |

