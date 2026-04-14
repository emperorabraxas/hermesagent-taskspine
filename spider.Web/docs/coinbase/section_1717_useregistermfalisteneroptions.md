# UseRegisterMfaListenerOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/UseRegisterMfaListenerOptions



Options for the useRegisterMfaListener hook.

## Properties

| Property         | Type                                  | Description                                                                                                                                                                                                         |
| ---------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `scope?`   | `RefObject`\<`null` \| `HTMLElement`> | Optional ref to a container element for scoped handling. When provided, the handler only responds to MFA triggers from within this element. When omitted, the handler responds to any MFA trigger (global handler). |
| <a /> `enabled?` | `boolean`                             | Whether the listener should be registered. When false, the listener is not registered. Useful for conditionally enabling/disabling the listener. **Default** `true`                                                 |

