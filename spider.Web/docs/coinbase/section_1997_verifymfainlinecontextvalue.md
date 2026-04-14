# VerifyMfaInlineContextValue
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaInlineContextValue



The context value for the VerifyMfaInline component.

## See

[useVerifyMfaInlineContext](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useVerifyMfaInlineContext)

## Properties

| Property            | Type                                                                                                                                         | Description                                                                   |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| <a /> `view`        | [`VerifyMfaInlineView`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/VerifyMfaInlineView)                                     | The current view of the inline MFA flow.                                      |
| <a /> `goToVerify`  | () => `void`                                                                                                                                 | A function to go to the verify view.                                          |
| <a /> `goToContent` | (`direction?`: [`VerifyMfaInlineDirection`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/VerifyMfaInlineDirection)) => `void` | A function to go to the content view. Optionally specify animation direction. |
| <a /> `goBack`      | () => `void`                                                                                                                                 | A function to go back to the previous view.                                   |

