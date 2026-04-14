# LinkAuthProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthProps



Props for the LinkAuth component

## See

[LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth)

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLDivElement`>, `"children"`>

## Properties

| Property               | Type                                                                                                                                   | Description                                                                                                                                                                                            |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a /> `children?`      | \| `ReactNode` \| (`state`: [`LinkAuthState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthState)) => `ReactNode` | The children of the component. Leave empty to use the default UI. If a function is provided, it will be called with the current state of the link auth flow. The function should return a `ReactNode`. |
| <a /> `onLinkSuccess?` | (`method`: \| `null` \| [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)) => `void`              | A function to call when an auth method is successfully linked.                                                                                                                                         |

