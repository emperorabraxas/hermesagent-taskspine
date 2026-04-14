# LinkAuthFlowContextValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthFlowContextValue



The value of the link auth flow context.

## See

[useLinkAuthFlow](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useLinkAuthFlow)

## Properties

| Property            | Type                                                                                                         | Description                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| <a /> `back`        | () => `void`                                                                                                 | A function to call when the back button is clicked.            |
| <a /> `direction?`  | `"left"` \| `"right"`                                                                                        | The direction of the flow transition.                          |
| <a /> `link`        | (`method`: [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)) => `void` | A function to call when the user links an auth method.         |
| <a /> `linkSuccess` | () => `void`                                                                                                 | A function to call when an auth method is successfully linked. |

