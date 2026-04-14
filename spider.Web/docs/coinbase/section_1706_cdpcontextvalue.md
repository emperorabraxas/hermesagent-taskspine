# CDPContextValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/CDPContextValue



Core context value interface for the CDP (Coinbase Developer Platform) provider.

## Properties

| Property              | Type                                                                                                      | Description                                                      |
| --------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| <a /> `isInitialized` | `boolean`                                                                                                 | Whether the CDP SDK has completed initialization                 |
| <a /> `currentUser`   | \| `null` \| [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/User)                   | The currently authenticated user, or null if not signed in       |
| <a /> `isSignedIn`    | `boolean`                                                                                                 | Convenience boolean indicating if there is an authenticated user |
| <a /> `config`        | [`Config`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Config)                            | The CDP config                                                   |
| <a /> `oauthState`    | \| `null` \| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/OAuthFlowState) | The current OAuth flow state                                     |

