# SendSolanaTransactionButtonProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SendSolanaTransactionButtonProps



The props for the SendSolanaTransactionButton component.

## See

[SendSolanaTransactionButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SendSolanaTransactionButton)

## Extends

* `Omit`\<[`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps), `"onError"`>

## Properties

| Property              | Type                                                                                                                                                                  | Description                                                                              | Inherited from      |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------- |
| <a /> `account`       | `string`                                                                                                                                                              | The Solana account to send the transaction from.                                         | -                   |
| <a /> `network`       | [`SendSolanaTransactionWithEndUserAccountBodyNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaTransactionWithEndUserAccountBodyNetwork) | The network to send the transaction on.                                                  | -                   |
| <a /> `onError?`      | (`error`: \| `Error` \| [`APIError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/APIError)) => `void`                                                       | A function to call when the transaction errors.                                          | -                   |
| <a /> `onSuccess?`    | (`signature`: `string`) => `void`                                                                                                                                     | A function to call when the transaction is successful.                                   | -                   |
| <a /> `transaction`   | `string`                                                                                                                                                              | The base64 encoded transaction to send.                                                  | -                   |
| <a /> `size?`         | [`ButtonSize`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonSize)                                                                                | The size of the button. Defaults to "md".                                                | `Omit.size`         |
| <a /> `asChild?`      | `boolean`                                                                                                                                                             | Set to true to use a custom element or component in place of the default button element. | `Omit.asChild`      |
| <a /> `fullWidth?`    | `boolean`                                                                                                                                                             | Whether the button should be full width.                                                 | `Omit.fullWidth`    |
| <a /> `isPending?`    | `boolean`                                                                                                                                                             | Whether the button state is pending.                                                     | `Omit.isPending`    |
| <a /> `pendingLabel?` | `ReactNode`                                                                                                                                                           | A label to render when the button state is pending.                                      | `Omit.pendingLabel` |
| <a /> `variant?`      | [`ButtonVariant`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonVariant)                                                                          | The variant of the button. Defaults to "primary".                                        | `Omit.variant`      |

