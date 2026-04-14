# MFA_PROTECTED_FUNCTIONS
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Variables/MFA_PROTECTED_FUNCTIONS



```ts theme={null}
const MFA_PROTECTED_FUNCTIONS: {
  signEvmHash: (options: SignEvmHashOptions) => Promise<SignEvmHashResult>;
  signEvmTransaction: (options: SignEvmTransactionOptions) => Promise<SignEvmTransactionResult>;
  signSolanaTransaction: (options: SignSolanaTransactionOptions) => Promise<SignSolanaTransactionResult>;
  sendEvmTransaction: (options: SendEvmTransactionOptions) => Promise<SendEvmTransactionResult>;
  sendSolanaTransaction: (options: SendSolanaTransactionOptions) => Promise<SendSolanaTransactionResult>;
  signEvmMessage: (options: SignEvmMessageOptions) => Promise<SignEvmHashResult>;
  signSolanaMessage: (options: SignSolanaMessageOptions) => Promise<SignSolanaMessageResult>;
  signEvmTypedData: (options: SignEvmTypedDataOptions) => Promise<SignEvmTypedDataResult>;
  sendUserOperation: (options: SendUserOperationOptions) => Promise<SendUserOperationResult>;
  exportEvmAccount: (options: ExportEvmAccountOptions) => Promise<ExportEvmAccountResult>;
  exportSolanaAccount: (options: ExportSolanaAccountOptions) => Promise<ExportSolanaAccountResult>;
  createEvmKeyExportIframe: (options: CreateKeyExportIframeOptions) => Promise<CreateKeyExportIframeResult>;
  createSolanaKeyExportIframe: (options: CreateKeyExportIframeOptions) => Promise<CreateKeyExportIframeResult>;
};
```

**`Internal`**

Map of MFA-protected functions to ensure type safety.
If a function is renamed, the import will fail and this file won't compile.

## Type declaration

| Name                                  | Type                                                                                                                                                                                                                                                                          |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `signEvmHash()`                 | (`options`: [`SignEvmHashOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmHashOptions)) => `Promise`\<[`SignEvmHashResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmHashResult)>                                         |
| <a /> `signEvmTransaction()`          | (`options`: [`SignEvmTransactionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmTransactionOptions)) => `Promise`\<[`SignEvmTransactionResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmTransactionResult)>             |
| <a /> `signSolanaTransaction()`       | (`options`: [`SignSolanaTransactionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignSolanaTransactionOptions)) => `Promise`\<[`SignSolanaTransactionResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignSolanaTransactionResult)> |
| <a /> `sendEvmTransaction()`          | (`options`: [`SendEvmTransactionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmTransactionOptions)) => `Promise`\<[`SendEvmTransactionResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmTransactionResult)>             |
| <a /> `sendSolanaTransaction()`       | (`options`: [`SendSolanaTransactionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaTransactionOptions)) => `Promise`\<[`SendSolanaTransactionResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaTransactionResult)> |
| <a /> `signEvmMessage()`              | (`options`: [`SignEvmMessageOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmMessageOptions)) => `Promise`\<[`SignEvmHashResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmHashResult)>                                   |
| <a /> `signSolanaMessage()`           | (`options`: [`SignSolanaMessageOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignSolanaMessageOptions)) => `Promise`\<[`SignSolanaMessageResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignSolanaMessageResult)>                 |
| <a /> `signEvmTypedData()`            | (`options`: [`SignEvmTypedDataOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmTypedDataOptions)) => `Promise`\<[`SignEvmTypedDataResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmTypedDataResult)>                     |
| <a /> `sendUserOperation()`           | (`options`: [`SendUserOperationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendUserOperationOptions)) => `Promise`\<[`SendUserOperationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendUserOperationResult)>                 |
| <a /> `exportEvmAccount()`            | (`options`: [`ExportEvmAccountOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportEvmAccountOptions)) => `Promise`\<[`ExportEvmAccountResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportEvmAccountResult)>                     |
| <a /> `exportSolanaAccount()`         | (`options`: [`ExportSolanaAccountOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportSolanaAccountOptions)) => `Promise`\<[`ExportSolanaAccountResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExportSolanaAccountResult)>         |
| <a /> `createEvmKeyExportIframe()`    | (`options`: [`CreateKeyExportIframeOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/CreateKeyExportIframeOptions)) => `Promise`\<[`CreateKeyExportIframeResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/CreateKeyExportIframeResult)>     |
| <a /> `createSolanaKeyExportIframe()` | (`options`: [`CreateKeyExportIframeOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/CreateKeyExportIframeOptions)) => `Promise`\<[`CreateKeyExportIframeResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/CreateKeyExportIframeResult)>     |

