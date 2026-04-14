# LinkAuthItemsProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthItemsProps



The props for the LinkAuthItems component.

## See

[LinkAuthItems](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthItems)

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLUListElement`>, `"children"`>

## Properties

| Property          | Type                                                                                                                               | Description                                         |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| <a /> `children?` | (`props`: [`LinkAuthItemProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthItemProps)) => `ReactNode`       | A render function for the auth method item.         |
| <a /> `onLink?`   | (`method`: [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)) => `void` \| `Promise`\<`void`> | A function to call when the link button is clicked. |

