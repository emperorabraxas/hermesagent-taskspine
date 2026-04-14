# LinkAuthState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthState



The state of the account linking component

## See

* [LinkAuthAction](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/LinkAuthAction)
* [LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth)

## Properties

| Property             | Type                                                                                                | Description                                                           |
| -------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| <a /> `authMethods`  | [`LinkAuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/LinkAuthMethod)\[]   | The auth methods with data about the user and whether they are linked |
| <a /> `error`        | `null` \| `string`                                                                                  | Error message if fetching linked accounts failed                      |
| <a /> `isPending`    | `boolean`                                                                                           | Whether the account linking is pending                                |
| <a /> `methodToLink` | \| `null` \| [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod) | The auth method to link                                               |

