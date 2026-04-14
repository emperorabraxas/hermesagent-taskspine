# VerifyMfaInlineProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaInlineProps



Props for the VerifyMfaInline component.

## See

[VerifyMfaInline](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaInline)

## Extends

* `HTMLAttributes`\<`HTMLDivElement`>

## Properties

| Property              | Type         | Description                                                                                                                                                                                                                                                    | Overrides                  |
| --------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| <a /> `children`      | `ReactNode`  | The component children. Should include VerifyMfaInlineFlow. Can optionally include VerifyMfaInlineBackButton outside the Flow.                                                                                                                                 | `HTMLAttributes.children`  |
| <a /> `verifyFirst?`  | `boolean`    | If true, forces MFA verification before showing content. Use this when you want users to verify BEFORE seeing the content. If false (default), content is shown first and MFA is triggered automatically when a protected action is called. **Default** `true` | -                          |
| <a /> `onVerified?`   | () => `void` | Called when MFA verification completes successfully.                                                                                                                                                                                                           | -                          |
| <a /> `onCancel?`     | () => `void` | Called when MFA verification is cancelled. If provided, a back/cancel action in the verify view will trigger this and transition back to content.                                                                                                              | -                          |
| <a /> `successDelay?` | `number`     | The delay in milliseconds before transitioning to content after successful verification. This allows users to see the success state before the transition. **Default** `500`                                                                                   | -                          |
| <a /> `className?`    | `string`     | Additional class name for the container.                                                                                                                                                                                                                       | `HTMLAttributes.className` |

