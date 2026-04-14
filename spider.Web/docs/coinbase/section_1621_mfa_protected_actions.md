# MFA_PROTECTED_ACTIONS
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Variables/MFA_PROTECTED_ACTIONS



```ts theme={null}
const MFA_PROTECTED_ACTIONS: (
  | "signEvmHash"
  | "signEvmTransaction"
  | "signSolanaTransaction"
  | "sendEvmTransaction"
  | "sendSolanaTransaction"
  | "signEvmMessage"
  | "signSolanaMessage"
  | "signEvmTypedData"
  | "sendUserOperation"
  | "exportEvmAccount"
  | "exportSolanaAccount"
  | "createEvmKeyExportIframe"
  | "createSolanaKeyExportIframe")[];
```

List of action names that require MFA verification when the user is enrolled.

These actions involve sensitive operations like signing transactions,
sending funds, or exporting private keys.

## Example

```typescript theme={null}
import { MFA_PROTECTED_ACTIONS } from '@coinbase/cdp-core';

console.log(MFA_PROTECTED_ACTIONS);
// ['signEvmHash', 'signEvmTransaction', 'signSolanaTransaction', ...]
```

