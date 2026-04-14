# VerifyMfaItemsProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaItemsProps



The props for the VerifyMfaItems component.

## See

[VerifyMfaItems](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaItems)

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLUListElement`>, `"children"` | `"onSelect"`>

## Properties

| Property          | Type                                                                                                                           | Description                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------- |
| <a /> `children?` | (`props`: [`VerifyMfaItemProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaItemProps)) => `ReactNode` | A render function for the MFA method item.    |
| <a /> `onSelect?` | (`method`: `"totp"` \| `"sms"`) => `void`                                                                                      | A function to call when a method is selected. |

