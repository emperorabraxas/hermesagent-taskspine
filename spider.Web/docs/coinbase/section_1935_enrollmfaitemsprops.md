# EnrollMfaItemsProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaItemsProps



The props for the EnrollMfaItems component.

## See

[EnrollMfaItems](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaItems)

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLUListElement`>, `"children"`>

## Properties

| Property          | Type                                                                                                                           | Description                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| <a /> `children?` | (`props`: [`EnrollMfaItemProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaItemProps)) => `ReactNode` | A render function for the MFA method item.              |
| <a /> `onSetUp?`  | (`method`: `"totp"` \| `"sms"`) => `void` \| `Promise`\<`void`>                                                                | A function to call when a method is selected for setup. |

