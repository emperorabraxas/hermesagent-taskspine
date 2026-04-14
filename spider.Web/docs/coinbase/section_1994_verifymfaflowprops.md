# VerifyMfaFlowProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/VerifyMfaFlowProps



Props for the VerifyMfaFlow component.

## Extends

* `Omit`\<`HTMLAttributes`\<`HTMLElement`>, `"children"`>

## Properties

| Property               | Type                                                                                                                                                                                        | Description                                                 | Overrides        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ---------------- |
| <a /> `autoFocus?`     | `boolean`                                                                                                                                                                                   | If set, will auto focus the form when the component mounts. | `Omit.autoFocus` |
| <a /> `animateHeight?` | `boolean`                                                                                                                                                                                   | If set, will animate the height of the component.           | -                |
| <a /> `children?`      | (`props`: \{ `step`: [`VerifyMfaStep`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/VerifyMfaStep); `method`: `"totp"` \| `"sms"`; `Content`: `ReactNode`; }) => `ReactNode` | The children of the component.                              | -                |

