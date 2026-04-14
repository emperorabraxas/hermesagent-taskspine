# CDPReactProviderProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/CDPReactProviderProps



CDPReactProviderProps

## Properties

| Property                   | Type                                                                                     | Description                                                                                                                                                                                   |
| -------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `config`             | [`Config`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/Config)           | The app configuration                                                                                                                                                                         |
| <a /> `name?`              | `string`                                                                                 | The provider name, i.e. to distinguish between multiple providers                                                                                                                             |
| <a /> `theme?`             | `Partial`\<[`Theme`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/Theme)> | The theme values to override                                                                                                                                                                  |
| <a /> `data-cdp-provider?` | `string`                                                                                 | Provider name for multi-provider coordination. Used internally by CDPReactProvider to identify which provider owns focused elements. If not provided, a unique ID is generated automatically. |

